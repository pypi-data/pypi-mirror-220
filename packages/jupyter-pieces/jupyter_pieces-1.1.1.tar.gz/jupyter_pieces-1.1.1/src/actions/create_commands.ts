import { CodeCell } from '@jupyterlab/cells';
import { ICommandPalette } from '@jupyterlab/apputils';
import createAsset from './create_asset';
import {
    DiscoveryDiscoverAssetsRequest,
    FullTextSearchRequest,
    SeededFile,
} from '../PiecesSDK/core';
import { Asset, SeededDiscoverableAsset } from '../PiecesSDK/common';
import ConnectorSingleton from '../connection/connector_singleton';
import Constants from '../const';
import {
    loadPieces,
    processAsset,
    processAssets,
} from '../connection/api_wrapper';
import PiecesCacheSingleton from '../cache/pieces_cache';
import Notifications from '../connection/notification_handler';
import ShareableLinksService from '../connection/shareable_link';
import copyToClipboard from '../ui/utils/copyToClipboard';
import { showOnboarding } from '../onboarding/showOnboarding';
import discoverSnippets from './discover_snippets';
import langExtToClassificationSpecificEnum from '../ui/utils/langExtToClassificationSpecificEnum';
import { SeededFragment } from '../PiecesSDK/connector';
import { defaultApp } from '../index';
import { getStored } from '../localStorageManager';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';
import { draft_asset } from './draft_asset';
import { refreshSnippets, searchBox } from '../ui/render/renderSearchBox';
import { drawSnippets, sortDropdown } from '../ui/views/create_snippet_view';

const config: ConnectorSingleton = ConnectorSingleton.getInstance();
const cache: PiecesCacheSingleton = PiecesCacheSingleton.getInstance();
const notifications: Notifications = Notifications.getInstance();
const linkService: ShareableLinksService = ShareableLinksService.getInstance();

export const createCommands = ({ palette }: { palette: ICommandPalette }) => {
    const { commands } = defaultApp;

    // Enrich Selection
    const enrich_selection_command = 'jupyter-pieces:enrich-selection';
    commands.addCommand(enrich_selection_command, {
        label: 'Enrich Selection via Pieces',
        caption: 'Add a description to your selection',
        execute: enrichSelection,
    });
    defaultApp.contextMenu.addItem({
        command: enrich_selection_command,
        selector: '.jp-Cell',
        rank: 101,
    });

    // Snippetize notebook
    const snippetize_command = 'jupyter-pieces:discover-snippets';
    commands.addCommand(snippetize_command, {
        label: 'Discover Snippets',
        caption: 'Save all Snippets in your Notebook to Pieces',
        execute: snippetizeNotebook,
    });
    palette.addItem({
        command: snippetize_command,
        category: 'Pieces for Developers',
    });

    // Onboarding command
    const onboarding_command = 'jupyter-pieces:open-onboarding';
    commands.addCommand(onboarding_command, {
        label: 'Pieces for Developers Onboarding',
        execute: showOnboarding,
    });
    palette.addItem({
        command: onboarding_command,
        category: 'Pieces for Developers',
    });

    // save active cell to pieces command
    const save_active_cell_command = 'jupyter-pieces:save-cell-to-pieces';
    commands.addCommand(save_active_cell_command, {
        label: 'Save Active Cell to Pieces',
        caption: 'Save the Active Cell to Pieces',
        execute: saveActiveCellToPieces,
    });
    defaultApp.contextMenu.addItem({
        command: save_active_cell_command,
        selector: '.jp-Cell',
        rank: 100,
    });

    const share_active_cell_command = 'jupyter-pieces:share-cell-via-pieces';
    commands.addCommand(share_active_cell_command, {
        label: 'Share Active Cell via Pieces',
        caption: 'Share the Active Cell via Pieces',
        execute: shareActiveCellViaPieces,
    });
    defaultApp.contextMenu.addItem({
        command: share_active_cell_command,
        selector: '.jp-Cell',
        rank: 100,
    });

    // save selection to pieces command
    const save_selection_to_pieces_command =
        'jupyter-pieces:save-selection-to-pieces';
    commands.addCommand(save_selection_to_pieces_command, {
        label: 'Save Selection to Pieces',
        caption: 'Save your Selection to Pieces',
        execute: saveSelectionToPieces,
    });
    defaultApp.contextMenu.addItem({
        command: save_selection_to_pieces_command,
        selector: '*',
        rank: 100,
    });

    const share_selection_via_pieces_command =
        'jupyter-pieces:share-selection-via-pieces';
    commands.addCommand(share_selection_via_pieces_command, {
        label: 'Share Selection via Pieces',
        caption: 'Share your Selection via Pieces',
        execute: shareSelectionViaPieces,
    });
    defaultApp.contextMenu.addItem({
        command: share_selection_via_pieces_command,
        selector: '*',
        rank: 100,
    });

    // Right-click menu
    commands.addCommand('text-shortcuts:save-selection-to-pieces', {
        label: 'Save Selection to Pieces',
        execute: saveSelectionToPieces,
    });
    commands.addCommand('text-shortcuts:share-selection-via-pieces', {
        label: 'Share Selection via Pieces',
        execute: shareSelectionViaPieces,
    });
    commands.addCommand('text-shortcuts:save-cell-to-pieces', {
        label: 'Save Active Cell to Pieces',
        execute: saveActiveCellToPieces,
    });
    commands.addCommand('text-shortcuts:share-cell-via-pieces', {
        label: 'Share Active Cell via Pieces',
        execute: shareActiveCellViaPieces,
    });

    // Refresh pieces - right click
    const refresh_snippets_command = 'text-shortcuts:refresh-snippets';
    commands.addCommand(refresh_snippets_command, {
        label: 'Refresh Snippets',
        execute: refreshPieces,
    });

    // Jump to searchbar of Pieces - keyboard command
    const quick_search_command = 'text-shortcuts:quick-search';
    commands.addCommand(quick_search_command, {
        label: 'Quick Search',
        execute: quickSearch,
    });

    // Toggle Pieces view - keyboard command
    const toggle_view_command = 'text-shortcuts:toggle-view';
    commands.addCommand(toggle_view_command, {
        label: 'Toggle View',
        execute: toggleView,
    });

    // Toggle Pieces view - keyboard command
    const snippetize_discover_command = 'text-shortcuts:discover-snippets';
    commands.addCommand(snippetize_discover_command, {
        label: 'Discover Snippets in Your Notebook',
        execute: snippetizeNotebook,
    });
};

const enrichSelection = async () => {
    const selection = document.getSelection();
    if (!selection || selection.toString().length < 5) {
        notifications.error({ message: Constants.NO_SAVE_SELECTION });
        return;
    }

    const draft_seed = await draft_asset({ text: selection.toString() });

    //@ts-ignore this does not exist in the api given by jupyterlab, however editor does exist if they have a notebook open.
    const editor = defaultApp.shell.currentWidget?.content.activeCell.editor;
    if (!editor || editor === undefined) {
        notifications.error({
            message: 'Unable to detect editor, cannot enrich.',
        });
        return;
    }

    // Define the text you want to insert
    const textToInsert = `'''\n${
        draft_seed.asset?.metadata?.description ?? ''
    }\n'''\n`;

    editor.replaceSelection(textToInsert + selection);

    // Move the cursor to the end of the inserted text
};

let inSnippetize = false;
const snippetizeNotebook = async () => {
    if (inSnippetize) {
        notifications.error({
            message:
                'We are already snippetizing your notebook! Just wait a bit.',
        });
        return;
    }
    inSnippetize = true;
    notifications.information({
        message: 'We are snippetizing your notebook! Sit tight!',
    });

    try {
        //@ts-ignore
        const cells = defaultApp.shell.currentWidget?.content?.cellsArray;
        if (!cells) {
            notifications.error({ message: Constants.DISCOVERY_FAILURE });
            return;
        }
        const discoverableAssets: DiscoveryDiscoverAssetsRequest = {
            automatic: true,
            seededDiscoverableAssets: {
                application: config.context.application.id,
                iterable: [],
            },
        };

        for (let i = 0; i < cells.length; i++) {
            if (!(cells[i] instanceof CodeCell)) {
                continue;
            }
            const raw = cells[i].model.toJSON().source;
            if (!raw) {
                continue;
            }
            const lang =
                //@ts-ignore
                defaultApp.shell.currentWidget?.sessionContext?.kernelPreference
                    ?.language;

            let discoverable: SeededDiscoverableAsset = {};

            let seed: SeededFile | SeededFragment = {
                string: {
                    raw: raw,
                },
                metadata: {
                    ext: langExtToClassificationSpecificEnum(lang),
                },
            };

            // if code cell is 50 lines or longer then upload it as a file so it gets 'snippetized'
            if (raw.split('\n').length > 50) {
                discoverable.file = seed;
            } else {
                discoverable.fragment = seed;
            }

            discoverableAssets.seededDiscoverableAssets?.iterable.push(
                discoverable
            );
        }
        if (!discoverableAssets.seededDiscoverableAssets?.iterable.length) {
            notifications.error({
                message:
                    "Something went wrong, we weren't able to find any snippets to discover",
            });
            return;
        }
        const returnedResults = await discoverSnippets(discoverableAssets);
        loadPieces().then(() => {
            drawSnippets({});
        });
        if (getStored('AutoOpen') && returnedResults?.iterable.length !== 0) {
            defaultApp.shell.activateById('piecesView');
        }
    } catch (e) {
        notifications.error({
            message:
                'Failed to snippetize notebook, are you sure Pieces OS is installed, running, and up to date?',
        });
    }

    inSnippetize = false;
};

const refreshPieces = () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_REFRESH_HOTKEY,
    });

    refreshSnippets();
};

const quickSearch = () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_QUICK_SEARCH_HOTKEY,
    });

    defaultApp.shell.activateById('piecesView');
    searchBox.focus();
};

const toggleView = () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_TOGGLE_VIEW_HOTKEY,
    });

    let newSelection = sortDropdown.selectedIndex + 1;
    if (newSelection >= sortDropdown.options.length) newSelection = 0; //Wrap back to 0

    sortDropdown.selectedIndex = newSelection;
};

export const saveActiveCellToPieces = async () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SAVE_ACTIVE_CELL,
    });

    // TODO very sad can't use typescript lsp magic D:
    //@ts-ignore
    const activeCell = defaultApp.shell.currentWidget?.content.activeCell;
    //@ts-ignore
    const cells = defaultApp.shell.currentWidget?.content?.cellsArray;
    //@ts-ignore
    const notebookName = defaultApp.shell.currentPath ?? 'unknown';
    let cellNum;

    if (!activeCell) {
        notifications.error({ message: Constants.NO_ACTIVE_CELL });
        return;
    } else if (!(activeCell instanceof CodeCell)) {
        notifications.error({ message: Constants.NO_CODE_CELL });
        return;
    }

    for (let i = 0; i < cells.length; i++) {
        if (cells[i] === activeCell) {
            cellNum = i;
            break;
        }
    }

    const code = activeCell.model.toJSON().source;
    if (code.length < 5) {
        notifications.error({
            message: 'There is no code saved in this cell!',
        });
        return;
    }
    try {
        const { similarity } = await findSimilarity(code);
        if (similarity < 2) {
            notifications.information({ message: Constants.SAVE_EXISTS });
        } else {
            await createAsset(
                code as string,
                false,
                `This snippet came from cell ${
                    (cellNum ?? -1) + 1
                } of ${notebookName}`
            );
            drawSnippets({});
        }
    } catch (e) {
        notifications.error({
            message:
                'Failed to save snippet to pieces, are you sure that Pieces OS is running?',
        });
    }
    if (getStored('AutoOpen')) {
        defaultApp.shell.activateById('piecesView');
    }
};

export const saveSelectionToPieces = async () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SAVE_SELECTION,
    });

    const selection = document.getSelection();
    //@ts-ignore
    const filename = defaultApp.shell.currentPath ?? 'unknown';
    if (!selection || selection.toString().length < 5) {
        notifications.error({ message: Constants.NO_SAVE_SELECTION });
        return;
    }
    try {
        await createAsset(
            selection.toString(),
            false,
            `This snippet was saved via selection from ${filename}`
        );
    } catch (e) {
        notifications.error({
            message:
                'Failed to save selection to Pieces. Are you sure Pieces OS is running?',
        });
    }
    drawSnippets({});
    if (getStored('AutoOpen')) {
        defaultApp.shell.activateById('piecesView');
    }
};

export const shareSelectionViaPieces = async () => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SHARE_SELECTION,
    });

    const selection = document.getSelection();
    if (!selection || selection.toString().length < 5) {
        notifications.error({ message: Constants.NO_SAVE_SELECTION });
        return;
    }

    try {
        const { similarity, comparisonID } = await findSimilarity(
            selection.toString()
        );
        if (similarity < 2) {
            if (typeof comparisonID === 'string') {
                const existingLink = processAsset({
                    asset: cache.mappedAssets[comparisonID],
                }).share;
                const link =
                    existingLink ??
                    (await linkService.generate({
                        id: comparisonID,
                    }));
                copyToClipboard(link || '');
                if (existingLink) {
                    notifications.information({
                        message: Constants.LINK_GEN_COPY,
                    });
                }
            }
        } else {
            await saveAndShare(selection.toString());
            drawSnippets({});
        }
    } catch (e) {
        notifications.error({
            message:
                'Failed to share selection via pieces, are you sure Pieces OS is running?',
        });
    }
};

export const shareActiveCellViaPieces = async () => {
    // TODO very sad can't use typescript lsp magic D:
    //@ts-ignore
    const activeCell = defaultApp.shell.currentWidget?.content.activeCell;
    //@ts-ignore
    const cells = defaultApp.shell.currentWidget?.content?.cellsArray;
    //@ts-ignore
    const notebookName = defaultApp.shell.currentPath ?? 'unknown';

    if (!activeCell) {
        notifications.error({ message: Constants.NO_ACTIVE_CELL });
        return;
    } else if (!(activeCell instanceof CodeCell)) {
        notifications.error({ message: Constants.NO_CODE_CELL });
        return;
    }

    let cellNum;
    for (let i = 0; i < cells.length; i++) {
        if (cells[i] === activeCell) {
            cellNum = i;
            break;
        }
    }

    const code = activeCell.model.toJSON().source;
    const { similarity, comparisonID } = await findSimilarity(code);

    if (similarity < 2) {
        if (typeof comparisonID === 'string') {
            const link = await linkService.generate({
                id: comparisonID,
            });
            copyToClipboard(link || '');
        }
    } else {
        const id = await createAsset(
            code as string,
            false,
            `This snippet came from cell ${
                (cellNum ?? -1) + 1
            } of ${notebookName}`
        );
        const link = await linkService.generate({
            id: id!,
        });
        copyToClipboard(link || '');
    }
    drawSnippets({});
};

/*
Handler for editor menu -> share snippet
    - creates a snippet
    - generates a link
    - copies to clipboard
*/
async function saveAndShare(selection: string) {
    const id = await createAsset(selection);
    if (typeof id === 'string') {
        const link = await linkService.generate({ id: id });
        copyToClipboard(link || '');
    }
}

export async function findSimilarity(
    codeBlock: string | string[]
): Promise<{ similarity: number; comparisonID: string }> {
    let comparisonScore = Infinity;
    let comparisonID = '';
    const rawCode: FullTextSearchRequest = {
        query: truncateAfterNewline(codeBlock),
    };

    const result = config.searchApi.fullTextSearch(rawCode);

    const assetArray: Asset[] = [];

    await result.then(
        async (res: { iterable: { identifier: string | number }[] }) => {
            res.iterable.forEach((element: { identifier: string | number }) => {
                assetArray.push(cache.mappedAssets[element.identifier]);
            });
            const returnedSnippets = await processAssets({
                assets: assetArray,
            });

            returnedSnippets.snippets.forEach((element) => {
                try {
                    // TODO: Make sure that `element.raw` is always going to be a string
                    const currentCompScore = calculateLevenshteinDistance(
                        codeBlock,
                        element.raw as string
                    );

                    if (currentCompScore < comparisonScore) {
                        comparisonScore = currentCompScore; // Update the current low number if the condition is true
                        comparisonID = element.id;
                    }
                } catch {
                    console.log('Error in calculating similarity score');
                }
            });
        }
    );
    return { similarity: comparisonScore, comparisonID: comparisonID };
}

function truncateAfterNewline(str: string | string[]): string {
    if (Array.isArray(str)) {
        str = str[0];
    }
    const newlineIndex = str.indexOf('\n');
    if (newlineIndex !== -1) {
        return str.substring(0, newlineIndex);
    } else {
        return str;
    }
}

function calculateLevenshteinDistance(
    str1: string | string[],
    str2: string
): number {
    if (Array.isArray(str1)) {
        str1 = str1.join('\n');
    }

    const m = str1.length;
    const n = str2.length;

    if (Math.abs(m - n) > 2) {
        return Infinity; // Distance exceeds threshold, exit early
    }
    const dp: number[][] = [];

    for (let i = 0; i <= m; i++) {
        dp[i] = [i];
    }

    for (let j = 1; j <= n; j++) {
        dp[0][j] = j;
    }

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1, // deletion
                    dp[i][j - 1] + 1, // insertion
                    dp[i - 1][j - 1] + 1 // substitution
                );
            }
        }
    }

    return dp[m][n];
}
