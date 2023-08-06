import PiecesCacheSingleton from '../cache/pieces_cache';
import { constructSnippet } from '../ui/views/renderListView';
import { loadConnect, processAsset } from './api_wrapper';
import { Asset, StreamedIdentifiers, Assets } from '../PiecesSDK/core';
import DedupeAssetQueue from './DedupeAssetQueue';
import { clearStaleIds, writeDB } from '../utils';
import {
    SortSnippetsBy,
    defaultSortingView,
    setDefaultSortingView,
} from '../ui/render/renderSearchBox';
import {
    drawSnippets,
    isFetchFailed,
    setIsFetchFailed,
} from '../ui/views/create_snippet_view';
import { redrawGpt } from '../ui/views/create_gpt_view';
import { SentryTracking } from '../analytics/SentryTracking';
import CheckVersionAndConnection from './checkVersionAndConnection';
let identifierWs: WebSocket;
const cache = PiecesCacheSingleton.getInstance();
const fetchQueue = new DedupeAssetQueue();
export let streamOpen = false;
let streamClosed = false;
export const waitTimer = 10_000;
export const setStreamOpen = (val: boolean) => {
    streamOpen = val;
};
export const stream = async () => {
    streamIdentifiers();
};

export function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

/*
	This establishes a websocket connection with POS
	on each event, we first check if it is a delete
	if it's a delete, remove the asset from UI and cache, then return
	if not, then we fetch the snapshot and formats related to that asset
	we then run checks to see if it is a new asset, or an updated asset,
	and then update ui + cache accordingly.
*/
const streamIdentifiers = async (): Promise<void> => {
    if (streamClosed) return;
    if (streamOpen) {
        return;
    }
    streamOpen = true;
    if (identifierWs?.readyState === identifierWs?.OPEN) {
        identifierWs?.close();
    }

    identifierWs = new WebSocket(
        'ws://localhost:1000/assets/stream/identifiers'
    );

    identifierWs.onclose = async () => {
        console.log('closed');
        if (!isFetchFailed) {
            setIsFetchFailed(true);
            drawSnippets({});
            redrawGpt();
        }
        await sleep(15_000);
        streamOpen = false;
        CheckVersionAndConnection.run().then(() => {
            streamIdentifiers();
        });
    };

    // update the ui when socket is established
    identifierWs.onopen = () => {
        loadConnect()
            .then(async () => {
                await SentryTracking.update();
            })
            .catch(() => {
                // do nothing
            });
        if (isFetchFailed) {
            setIsFetchFailed(false);
            drawSnippets({});
            redrawGpt();
        }

        clearStaleIds();
    };

    identifierWs.onmessage = async (event) => {
        const assets = JSON.parse(event.data) as StreamedIdentifiers;

        for (let i = 0; i < assets.iterable.length; i++) {
            if (assets.iterable[i].deleted) {
                const snippetEl = document.getElementById(
                    `snippet-el-${assets.iterable[i].asset!.id}`
                );
                snippetEl?.remove();

                // remove from cache
                delete cache.mappedAssets[assets.iterable[i].asset!.id];
                const indx = cache.assets.findIndex(
                    (e) => e.id === assets.iterable[i].asset!.id
                );
                if (indx >= 0) {
                    // <-- this check is somewhat redundant but why not be safe
                    cache.assets = [
                        ...cache.assets.slice(0, indx),
                        ...cache.assets.slice(indx + 1),
                    ];
                    writeDB();
                    if (!cache.assets.length) {
                        setDefaultSortingView(SortSnippetsBy.Recent);
                        drawSnippets({});
                    } else if (defaultSortingView === SortSnippetsBy.Language) {
                        langReset();
                    }
                }
                continue;
            }

            fetchQueue.push(assets.iterable[i].asset!.id);
        }
    };
};

export const closeStreams = async () => {
    streamClosed = true;
    identifierWs?.close();
};

/*
	Forewarning: somewhat complex
	This receives assets from the fetch queue and updates the dom accordingly
	first make sure to remove the loading / 0 snippet divs
	then update snippet list element(s)
*/
export const renderFetched = async ({ assets }: { assets: Assets }) => {
    const loadingDivs = document.querySelectorAll('.loading-div');
    loadingDivs.forEach((loadingDiv) => {
        loadingDiv.remove();
    });

    const emptyDivs = document.querySelectorAll('.pieces-empty-state');
    emptyDivs.forEach((div) => {
        div.remove();
    });

    const newDivs = document.querySelectorAll('.new-div');
    newDivs.forEach((newDiv) => {
        newDiv.remove();
    });

    if (newDivs.length || loadingDivs.length) {
        const onlyDiv = document.querySelectorAll('.only-snippet');
        onlyDiv.forEach((el) => {
            el.remove();
        });
        // commenting this out because i think it's causing more issues than it solves.
        //await triggerUIRedraw(false, undefined, undefined, false);
    }
    const sortedAssets = cache.assets.sort(
        (a, b) => b.created.value.getTime() - a.created.value.getTime()
    );

    assets.iterable.forEach((element: Asset) => {
        const cachedAsset = cache.mappedAssets[element.id];
        //new asset
        if (!cachedAsset) {
            cache.prependAsset({ asset: element });

            const processed = processAsset({ asset: element });

            // Need to update the Map
            const newMap = cache.snippetMap.get(processed.language);
            // If the language map does not exist, create it
            if (!newMap) {
                cache.snippetMap.set(processed.language, [processed.id]);
            } else {
                newMap.unshift(processed.id);
                cache.snippetMap.set(processed.language, newMap);
            }

            // Map is updated, now update the UI

            if (defaultSortingView === SortSnippetsBy.Recent) {
                const parentEl = document.getElementById(
                    'pieces-snippet-container'
                ) as HTMLDivElement;
                const processed = processAsset({ asset: element });

                const newIndex = sortedAssets.findIndex(
                    (asset) =>
                        asset.created.value.getTime() <
                        processed.created.getTime()
                );

                // Create the new element
                const newElement = constructSnippet(processed);

                // Insert the new element at the proper index
                if (newIndex === -1) {
                    // If newIndex is -1, it means the new element should be the oldest, so append it.
                    parentEl.appendChild(newElement);
                } else {
                    // Insert the new element before the element at the newIndex.
                    parentEl.insertBefore(
                        newElement,
                        parentEl.children[newIndex - 1]
                    );
                }
            } else if (defaultSortingView === SortSnippetsBy.Language) {
                if (!cache.assets.length) {
                    setDefaultSortingView(SortSnippetsBy.Recent);
                    drawSnippets({});
                } else if (defaultSortingView === SortSnippetsBy.Language) {
                    langReset();
                }
            }
        }

        //updated asset
        else if (
            new Date(cachedAsset?.updated.value).getTime() <
            new Date(element.updated.value).getTime()
        ) {
            const processed = processAsset({ asset: element });

            // Get the original snippet
            const originalSnippet = processAsset({
                asset: cache.mappedAssets[element.id],
            });

            if (
                processed.description === originalSnippet.description &&
                processed.raw === originalSnippet.raw &&
                processed.title === originalSnippet.title &&
                processed.language === originalSnippet.language &&
                processed.share === originalSnippet.share
            ) {
                return;
            }

            // Need to remove the old asset from the map
            const oldMapKeyValues = cache.snippetMap.get(
                originalSnippet.language
            );

            if (oldMapKeyValues) {
                oldMapKeyValues.forEach((snippetId) => {
                    if (snippetId === element.id) {
                        oldMapKeyValues.splice(
                            oldMapKeyValues.indexOf(snippetId),
                            1
                        );
                    }
                });
                if (oldMapKeyValues.length === 0) {
                    cache.snippetMap.delete(originalSnippet.language);
                } else {
                    cache.snippetMap.set(
                        originalSnippet.language,
                        oldMapKeyValues
                    );
                }
            }

            // Need to add the new asset to the map
            let inLangMap = false;
            const newMapkeyValues = cache.snippetMap.get(processed.language);
            if (newMapkeyValues) {
                // Check to make sure it's not already in the map
                newMapkeyValues.forEach((snippetId) => {
                    if (snippetId === processed.id) {
                        inLangMap = true;
                    }
                });
                // If it's not in the map, add it
                if (!inLangMap) {
                    newMapkeyValues.unshift(processed.id);
                    cache.snippetMap.set(processed.language, newMapkeyValues);
                }
            } else {
                cache.snippetMap.set(processed.language, [processed.id]);
            }

            // Map is updated, now update the UI

            cache.updateAsset({ asset: element });

            if (defaultSortingView === SortSnippetsBy.Recent) {
                const snippetEl = document.getElementById(
                    `snippet-el-${element.id}`
                );
                const opened = (
                    snippetEl?.children[0].lastChild
                        ?.firstChild as HTMLInputElement
                )?.checked;
                snippetEl?.replaceWith(
                    constructSnippet(processed, false, opened)
                );
            } else if (defaultSortingView === SortSnippetsBy.Language) {
                if (
                    (processed.description !== originalSnippet.description ||
                        processed.raw !== originalSnippet.raw ||
                        processed.title !== originalSnippet.title ||
                        processed.share !== originalSnippet.share) &&
                    processed.language === originalSnippet.language
                ) {
                    // const parentEl = (
                    //     document.getElementById(
                    //         'code-view-' + langExtToReadable(processed.language)
                    //     ) as HTMLDivElement
                    // ).firstChild?.lastChild as HTMLDivElement;
                    const snippetEl = document.getElementById(
                        `snippet-el-${element.id}`
                    );
                    const opened = (
                        snippetEl?.children[0].lastChild
                            ?.firstChild as HTMLInputElement
                    )?.checked;
                    snippetEl?.replaceWith(
                        constructSnippet(processed, false, opened)
                    );
                    return;
                }
                langReset();
            }
        }
    });
    writeDB();
};

const langReset = async () => {
    const openLangs: string[] = [];
    // Get all open language views
    const langContainers = Array.from(
        document.querySelectorAll('.language-button-input')
    );

    langContainers.forEach((langContainer) => {
        if ((langContainer as HTMLInputElement).checked) {
            openLangs.push(langContainer.id);
        }
    });

    await drawSnippets({});

    openLangs.forEach((langId) => {
        try {
            const snippetContentParent = document.getElementById(
                langId
            ) as HTMLInputElement;
            // there should only be a single parent element found
            snippetContentParent.checked = true;
            const clickEvent = new Event('change');
            snippetContentParent?.dispatchEvent(clickEvent);
        } catch (e) {
            // do nothing
        }
    });
};
