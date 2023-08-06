import ConnectorSingleton from '../connection/connector_singleton';
import PiecesCacheSingleton from '../cache/pieces_cache';
import { returnedSnippet } from '../typedefs';
import { processAssets } from '../connection/api_wrapper';
import Constants from '../const';
import { SearchedAssets } from '../PiecesSDK/core';
import { PromiseResolution } from '../utils';
import Notifications from '../connection/notification_handler';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';

const config: ConnectorSingleton = ConnectorSingleton.getInstance();
//const notifications: Notifications = Notifications.getInstance()
const storage: PiecesCacheSingleton = PiecesCacheSingleton.getInstance();
const notifications: Notifications = Notifications.getInstance();

// TODO for randy to convert this to a singleton, or a class with a static variable for the searching promis resolution.
let searching:
    | {
          resolution: {
              resolver: (args: SearchedAssets) => void | SearchedAssets;
              rejector: (args: SearchedAssets) => void | SearchedAssets;
              promise: Promise<SearchedAssets>;
          };
          query: string;
      }
    | undefined;

const shuffle = <returnedSnippet>(array: returnedSnippet[]) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
};

const shuffleAndReinsert = <returnedSnippet>(
    array: returnedSnippet[]
): returnedSnippet[] => {
    const elementsToTake = Math.min(5, array.length); // Take up to five elements or the length of the array, whichever is smaller
    const takenElements = shuffle(array.splice(0, elementsToTake)); // Take the first few elements from the array
    takenElements.concat(array); // Concatenate the shuffled elements with the rest of the array
    return takenElements;
};

export const search = async ({
    query,
}: {
    query: string;
}): Promise<returnedSnippet[]> => {
    // TODO think about rapid behavior, ie if this gets called many times do we want to reject the current search or wait until it is done?
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SEARCH,
    });

    try {
        // if we havent defined our resolver then define one.
        if (searching) {
            // here one is already defined, so we have options here.
            // option 1: we can reject the current search and start a new one.
            // option 2: we can wait untill the current search is done and then start a new one.
            // ans: go with option 1;
            searching.resolution.rejector({
                iterable: [],
                suggested: 0,
                exact: 0,
            });
        }

        // reset the searching object, no matter what.
        searching = {
            query,
            resolution: PromiseResolution<SearchedAssets>(),
        };

        // declare a global searchingResolver. (PromiseResolution)
        // this is gonna give 3 things.
        // (1) a promise: This will be used to conrol execution of this search.
        // (2) a resolver: this will NEED to get called when the search completes and it is a success
        // (3) a rejector: this will need to get called when (1) there is an error in the search, or (2) if we want to cancel the search.

        // call this sync, this is super important.
        config.assetsApi
            .assetsSearchAssets({
                query: query,
                transferables: false,
            })
            .then((response) => {
                if (!searching) {
                    return response;
                }
                searching.resolution.resolver(response);
            })
            .catch((e) => {
                if (!searching) {
                    return { iterable: [], suggested: 0, exact: 0 };
                }

                searching.resolution.rejector({
                    iterable: [],
                    suggested: 0,
                    exact: 0,
                });
            });

        // we are going to indefinetly untill the promise is compkleted in some way shape or form.
        // TODO veify that the parent catch gets fired when we reject the search.
        const results: SearchedAssets = await searching.resolution.promise;

        // once we are completely done searching, just ensure that we rest our promise resolution.
        searching = undefined;

        const assets = storage.assets;
        const returnedResults = [];

        let found_asset;
        for (const asset of results.iterable) {
            found_asset = undefined;
            found_asset = assets.find((e) => e.id === asset.identifier);
            if (found_asset) {
                returnedResults.push(found_asset);
            }
        }

        if (returnedResults.length < 5 && returnedResults.length != 0) {
            // Try Neural Code Search
            searching = {
                query,
                resolution: PromiseResolution<SearchedAssets>(),
            };

            // Neural Code Search
            config.searchApi
                .neuralCodeSearch({
                    query: query,
                })
                .then((response) => {
                    if (!searching) {
                        return response;
                    }
                    searching.resolution.resolver(response);
                })
                .catch((e) => {
                    if (!searching) {
                        return { iterable: [], suggested: 0, exact: 0 };
                    }

                    searching.resolution.rejector({
                        iterable: [],
                        suggested: 0,
                        exact: 0,
                    });
                });

            // we are going to search indefinetly until the promise is completed in some way shape or form.
            // TODO veify that the parent catch gets fired when we reject the search.
            const results: SearchedAssets = await searching.resolution.promise;
            searching = undefined;

            for (const asset of results.iterable) {
                found_asset = undefined;
                found_asset = storage.assets.find(
                    (e) => e.id === asset.identifier
                );
                if (found_asset && !returnedResults.includes(found_asset)) {
                    returnedResults.push(found_asset);
                }
            }
        }

        const snippets = (await processAssets({ assets: returnedResults }))
            .snippets;
        notifications.information({
            message: `Search for '${query}' found ${snippets.length} result(s).`,
        });

        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_SEARCH_SUCCESS,
        });

        return shuffleAndReinsert(snippets); // Lol, for Tsavo
    } catch (error) {
        // once we are completely done searching, just ensure that we rest our promise resolution.(even if it fails.)
        searching = undefined;

        const snippets = (await processAssets({ assets: storage.assets }))
            .snippets;
        notifications.error({ message: Constants.SEARCH_FAILURE });

        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_SEARCH_FAILURE,
        });

        return snippets;
    }
};
