import PiecesCacheSingleton from '../cache/pieces_cache';
import { processAsset } from '../connection/api_wrapper';
import { returnedSnippet } from '../typedefs';
import { searchLangSpecificEnum } from '../ui/utils/searcLangSpecificEnum';
import { getIcon } from '../ui/utils/langExtToIcon';
import { constructSnippet } from '../ui/views/renderListView';
import { renderListView } from '../ui/views/renderListView';

const cache = PiecesCacheSingleton.getInstance();

export async function updateLanguageView({
    snippetId,
    originalSnippet,
    inLangMap,
}: {
    snippetId: string;
    originalSnippet: returnedSnippet | undefined;
    inLangMap: boolean;
}) {
    // Language View Needs to Be Updated

    // Get the snippet from the cache
    const updatedSnippet = processAsset({
        asset: cache.mappedAssets[snippetId],
    });

    if (originalSnippet) {
        // Get the old input element
        const oldInputEl = document.getElementById(
            'input-' + searchLangSpecificEnum[originalSnippet.language]
        );

        // If it was open, remove the old element, the map handle should've already happened by now.
        if (oldInputEl && (oldInputEl as HTMLInputElement).checked) {
            const removalEl = document.getElementById(
                'list-view-' + originalSnippet.id
            );
            removalEl?.remove();
        }

        // How many snippets are remaining?
        const remainingSnippets = cache.snippetMap.get(
            originalSnippet.language
        );

        // If no snippets are left in that langView - remove it.
        if (!remainingSnippets || remainingSnippets.length === 0) {
            document
                .getElementById(
                    'code-view-' +
                        searchLangSpecificEnum[originalSnippet.language]
                )
                ?.remove();
        }
    }

    // Try to get the new input element
    const newInputEl = document.getElementById(
        'input-' + searchLangSpecificEnum[updatedSnippet.language]
    );

    // If it exists and is open
    if (newInputEl && (newInputEl as HTMLInputElement).checked) {
        // If it wasn't in the map, add it to the UI
        if (!inLangMap) {
            const parentEl = document.getElementById(
                'code-view-' + searchLangSpecificEnum[updatedSnippet.language]
            )?.lastChild as HTMLDivElement;
            parentEl?.prepend(constructSnippet(updatedSnippet, false));
        }
    }
    // Input doesn't exist and we need to build it.
    else {
        const snippetContainer = document.getElementById(
            'language-snippet-container'
        ) as HTMLDivElement;

        const CodeView = document.createElement('div');
        snippetContainer.appendChild(CodeView);
        CodeView.classList.add('code-view');
        CodeView.id =
            'code-view-' + searchLangSpecificEnum[updatedSnippet.language];

        // Create a title element
        const titleDiv = document.createElement('div');
        CodeView.appendChild(titleDiv);
        titleDiv.classList.add('code-title-div');

        const imageLang = document.createElement('img');
        titleDiv.appendChild(imageLang);
        const iconImage = getIcon(updatedSnippet.language);
        imageLang.setAttribute('src', iconImage);
        imageLang.setAttribute('alt', 'Code language logo');
        imageLang.classList.add('code-title-div');

        const title = document.createElement('h1');
        titleDiv.appendChild(title);
        title.innerText = searchLangSpecificEnum[updatedSnippet.language];
        title.classList.add('code-title-div');

        const buttonContentOpen = document.createElement('span');
        titleDiv.appendChild(buttonContentOpen);
        buttonContentOpen.innerText = '⌄';
        buttonContentOpen.classList.add('code-title-div');

        const buttonContentClosed = document.createElement('span');
        titleDiv.appendChild(buttonContentClosed);
        buttonContentClosed.innerText = '›';
        buttonContentClosed.classList.add('code-title-div');

        const buttonInput = document.createElement('input');
        buttonInput.setAttribute('type', 'checkbox');
        titleDiv.appendChild(buttonInput);
        buttonInput.classList.add('code-button-input');
        buttonInput.id =
            'input-' + searchLangSpecificEnum[updatedSnippet.language];

        if (buttonInput.checked) {
            titleDiv.removeChild(buttonContentClosed);
        } else {
            titleDiv.removeChild(buttonContentOpen);
        }

        let newCodeView: HTMLElement;

        buttonInput.addEventListener('click', function () {
            if (buttonInput.checked) {
                const snippetsInRange =
                    cache.snippetMap.get(updatedSnippet.language) ?? [];
                // Checkbox is checked, do something
                for (let i = 0; i < snippetsInRange.length; i++) {
                    if (!cache.mappedAssets[snippetsInRange[i]]) {
                        snippetsInRange.splice(i, 1);
                    }
                }
                const assetsInRange = snippetsInRange.map(
                    (snippetId: string) => {
                        return processAsset({
                            asset: cache.mappedAssets[snippetId],
                        });
                    }
                );
                newCodeView = renderListView({
                    container: snippetContainer,
                    snippets: assetsInRange.sort(
                        (a: returnedSnippet, b: returnedSnippet) =>
                            b.created.getTime() - a.created.getTime()
                    ),
                });
                CodeView.appendChild(newCodeView);
                titleDiv.removeChild(buttonContentClosed);
                titleDiv.appendChild(buttonContentOpen);
            } else {
                // Checkbox is unchecked, do something
                newCodeView.innerHTML = '';
                CodeView.removeChild(newCodeView);
                titleDiv.removeChild(buttonContentOpen);
                titleDiv.appendChild(buttonContentClosed);
            }
        });
    }
}
