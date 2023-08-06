import { LabIcon } from '@jupyterlab/ui-components';
import { AnalyticsEnum } from '../../analytics/AnalyticsEnum';
import { SegmentAnalytics } from '../../analytics/SegmentAnalytics';
import Constants from '../../const';
import { renderLoading } from './renderSnippets';
import { loadPieces } from '../../connection/api_wrapper';
import { search } from '../../actions/search';
import { drawSnippets, isFetchFailed } from '../views/create_snippet_view';
import { versionValid } from '../../connection/version_check';

export enum SortSnippetsBy {
    Recent,
    Language,
}

let defaultSearchQuery = '';

export const searchBox = document.createElement('input');
const searchBtn = document.createElement('button');
let searchCancelled = false;
export let defaultSortingView = SortSnippetsBy.Recent;

const refreshIcon = new LabIcon({
    name: 'jupyter-pieces:refresh',
    svgstr: Constants.REFRESH_SVG,
});

const cancelIcon = new LabIcon({
    name: 'jupyter-pieces:cancel',
    svgstr: Constants.CANCEL_SVG,
});

export const setDefaultSortingView = (val: SortSnippetsBy) => {
    defaultSortingView = val;
};

export const refreshSnippets = async () => {
    const loading = renderLoading(document, 'refresh-');

    if (searchBtn.parentElement)
        searchBtn.parentElement!.replaceChild(loading, searchBtn);

    try {
        await loadPieces();
        drawSnippets({});
    } catch (e) {
        console.log(e);
    }
    if (loading.parentElement)
        loading.parentElement!.replaceChild(searchBtn, loading);
};

export const handleSearch = async ({
    query,
}: {
    query: string;
}): Promise<void> => {
    if (query === '' || defaultSearchQuery === query) {
        return;
    }
    defaultSearchQuery = query;
    searchBox.value = query;
    const result = await search({ query: query });
    if (searchCancelled) {
        searchCancelled = false;
        return;
    }
    await drawSnippets({ snippets: result, search: true });
};

export const searchBoxElement = (): HTMLElement => {
    const searchRow = document.createElement('div');
    searchRow.classList.add('row', 'search-row');

    const inputCol = document.createElement('div');
    inputCol.classList.add('col');

    searchBox.classList.add('search-input', 'jp-input');
    searchBox.type = 'text';
    searchBox.placeholder = '🔍  Search for Snippets...';
    searchBox.value = '';
    searchBox.readOnly = !versionValid || isFetchFailed ? true : false;

    inputCol.appendChild(searchBox);
    searchRow.appendChild(inputCol);

    const searchBtnCol = document.createElement('div');
    searchBtnCol.classList.add('col');
    searchBtnCol.classList.add('col-sm');

    searchBtn.title = 'Refresh snippets';
    searchBtn.classList.add('pieces-btn-search', 'jp-btn');

    searchBox.value === ''
        ? refreshIcon.element({ container: searchBtn })
        : cancelIcon.element({ container: searchBtn });
    searchBtn.addEventListener('click', async () => {
        if (searchBox.value === '') {
            SegmentAnalytics.track({
                event: AnalyticsEnum.JUPYTER_REFRESH_CLICKED,
            });
            defaultSearchQuery = '';
            refreshSnippets();
        } else {
            // this.searchCancelled = true; // TODO ADD LOGIC FOR CANCEL
            searchBox.value = '';
            defaultSearchQuery = '';
            refreshIcon.element({ container: searchBtn });
            searchBtn.title = 'Refresh snippets';
            drawSnippets({});
        }
    });

    searchBox.addEventListener('keyup', async (event) => {
        if (event.key === 'Enter' && searchBox.value != '') {
            const loading = renderLoading(document, 'refresh-');
            searchBtnCol.replaceChild(loading, searchBtn);
            try {
                await handleSearch({ query: searchBox.value });
                cancelIcon.element({ container: searchBtn });
                searchBtn.title = 'Clear Search';
            } catch (e) {
                console.log(e);
            }
            searchBtnCol.replaceChild(searchBtn, loading);
        }
    });
    searchBtnCol.appendChild(searchBtn);
    searchRow.appendChild(searchBtnCol);

    return searchRow;
};

export const sortSnippetsDropdownElement = (): HTMLSelectElement => {
    const dropdownElement = document.createElement('select');
    dropdownElement.classList.add('jp-dropdown');

    const option_recent = document.createElement('option');
    option_recent.value = 'recent';
    option_recent.innerText = '🕓 RECENT';
    dropdownElement.appendChild(option_recent);

    const option_language = document.createElement('option');
    option_language.value = 'language';
    option_language.innerText = '🌐 LANGUAGE';
    dropdownElement.appendChild(option_language);

    dropdownElement.addEventListener('change', async () => {
        if (dropdownElement.value === 'language') {
            setDefaultSortingView(SortSnippetsBy.Language);
        } else if (dropdownElement.value === 'recent') {
            setDefaultSortingView(SortSnippetsBy.Recent);
        }

        if (searchBox.value === '') {
            drawSnippets({});
        } else {
            await handleSearch({ query: searchBox.value });
        }
    });

    return dropdownElement;
};

const codeSVG = new LabIcon({
    name: 'jupyter-pieces:codeSVG',
    svgstr: Constants.CODE_SVG,
});

const aiSVG = new LabIcon({
    name: 'jupyter-pieces:aiSVG',
    svgstr: Constants.AI_SVG,
});

export const renderNavBar = ({
    containerVar,
}: {
    containerVar: Element;
}): HTMLDivElement => {
    const backgroundDiv = document.createElement('div');
    backgroundDiv.classList.add('background');
    containerVar.appendChild(backgroundDiv);

    const wrapperDiv = document.createElement('div');
    wrapperDiv.classList.add('wrapper');
    containerVar.appendChild(wrapperDiv);

    const tabsDiv = document.createElement('div');
    wrapperDiv.appendChild(tabsDiv);
    tabsDiv.classList.add('tabs');
    tabsDiv.id = 'piecesTabs';

    const tabInput1 = document.createElement('input');
    tabsDiv.appendChild(tabInput1);
    tabInput1.type = 'radio';
    tabInput1.id = 'radio-1';
    tabInput1.name = 'tabs-1';

    tabInput1.checked = true;

    const tabLabel1 = document.createElement('label');
    tabsDiv.appendChild(tabLabel1);
    tabLabel1.htmlFor = 'radio-1';
    tabLabel1.classList.add('tab');
    tabLabel1.id = 'tab-1';

    codeSVG.element({ container: tabLabel1 });

    const tabInput2 = document.createElement('input');
    tabsDiv.appendChild(tabInput2);
    tabInput2.type = 'radio';
    tabInput2.id = 'radio-2';
    tabInput2.name = 'tabs-2';

    // tabInput2.checked = true;

    const tabLabel2 = document.createElement('label');
    tabsDiv.appendChild(tabLabel2);
    tabLabel2.htmlFor = 'radio-2';
    tabLabel2.classList.add('tab');
    tabLabel2.id = 'tab-2';

    aiSVG.element({ container: tabLabel2 });

    const slider = document.createElement('span');
    tabsDiv.appendChild(slider);
    slider.classList.add('glider');

    return wrapperDiv;
};
