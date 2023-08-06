import PiecesCacheSingleton from '../../cache/pieces_cache';
import { processAssets } from '../../connection/api_wrapper';
import versionCheck from '../../connection/version_check';
import { returnedSnippet } from '../../typedefs';
import {
    SortSnippetsBy,
    defaultSortingView,
    searchBoxElement,
    sortSnippetsDropdownElement,
} from '../render/renderSearchBox';
import { showLoadErrorState } from '../render/showLoadErrorState';
import { showLoadingState } from '../render/showLoadingState';
import { showNoSnippetState } from '../render/showNoSnippetState';
import { renderLanguageView } from './renderLanguageView';
import { renderListView } from './renderListView';

const cache: PiecesCacheSingleton = PiecesCacheSingleton.getInstance();
const containerDiv = document.createElement('div'); // Holding Div

export const sortDropdown = sortSnippetsDropdownElement();
export let isLoading = true;
export let isFetchFailed = false;

export const setIsLoading = (val: boolean) => {
    isLoading = val;
};

export const setIsFetchFailed = (val: boolean) => {
    isFetchFailed = val;
};

export const createSnippetListView = async ({
    containerVar,
}: {
    containerVar: Element;
    snippets: returnedSnippet[];
    viewType: SortSnippetsBy;
    searched?: boolean;
}) => {
    //Add the search box
    containerVar.id = 'piecesContainer';
    containerVar.classList.add('pieces-container');

    const searchBoxDiv = document.createElement('div');
    searchBoxDiv.classList.add('search-box-div');
    searchBoxDiv.appendChild(searchBoxElement());

    const dropdownRow = document.createElement('div');
    dropdownRow.classList.add('row', 'search-row');

    dropdownRow.appendChild(sortDropdown);

    const option_arrow = document.createElement('span');
    option_arrow.innerText = '▼';
    option_arrow.classList.add('jp-dropdown-arrow');
    dropdownRow.appendChild(option_arrow);

    searchBoxDiv.appendChild(dropdownRow);

    containerVar.appendChild(searchBoxDiv);

    drawSnippets({});
    containerVar.appendChild(containerDiv);
    containerDiv.classList.add('container-div');
    containerDiv.id = 'pieces-snippet-container';
};

// Make sure you call create view before calling this
//   - this is also called by createview
// Call this to redraw the view
export const drawSnippets = async ({
    snippets,
    search,
}: {
    snippets?: returnedSnippet[];
    search?: boolean;
}) => {
    containerDiv.innerHTML = '';
    containerDiv.classList.remove('load-error-state');
    console.log('Pieces For Developers: Redrawing');

    //Set up the loading state
    if (isLoading) {
        showLoadingState(containerDiv);
        return;
    }

    if (isFetchFailed || !(await versionCheck({}))) {
        showLoadErrorState(containerDiv);
        return;
    }

    if (cache.assets.length === 0) {
        showNoSnippetState(containerDiv);
        return;
    }

    let piecesSnippets =
        snippets !== undefined
            ? snippets
            : (
                  await processAssets({
                      assets: cache.assets,
                  })
              ).snippets;

    if (defaultSortingView === SortSnippetsBy.Recent) {
        renderListView({
            container: containerDiv,
            snippets: search
                ? piecesSnippets
                : piecesSnippets.sort(
                      (a, b) => b.created.getTime() - a.created.getTime()
                  ),
        });
    } else if (defaultSortingView === SortSnippetsBy.Language) {
        renderLanguageView({
            container: containerDiv,
            snippets: search
                ? piecesSnippets
                : piecesSnippets.sort((a, b) =>
                      a.language.localeCompare(b.language)
                  ),
        });
    }
};
