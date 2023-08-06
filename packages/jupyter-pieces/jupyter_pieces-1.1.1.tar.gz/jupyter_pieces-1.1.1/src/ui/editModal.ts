import { ClassificationSpecificEnum } from '../PiecesSDK/core';
import { returnedSnippet } from '../typedefs';
import langExtToReadable from './utils/langExtToReadable';
import { reclassify, update } from '../actions/update_asset';
import { highlightSnippet } from './utils/loadPrism';
import Notifications from '../connection/notification_handler';
import ConnectorSingleton from '../connection/connector_singleton';

const notifications = Notifications.getInstance();

export default async function showEditModal(snippet: returnedSnippet) {
    const editedContent = {
        id: snippet.id,
        title: snippet.title,
        description: snippet.description ?? '',
        language: snippet.language,
    };

    //ROOT DIV
    const main = document.getElementById('main');

    // MODAL CONTAINER
    const modalContainer = document.createElement('div');
    modalContainer.classList.add('edit-modal-container');

    // MODAL BACKGROUND
    const modalBackground = document.createElement('div');
    modalBackground.classList.add('edit-modal-background');

    //MODAL PARENT(S)
    const editModal = document.createElement('div');
    editModal.classList.add('edit-modal');

    //CLOSE BUTTON
    const modalCloseButtonDiv = document.createElement('div');
    modalCloseButtonDiv.classList.add('edit-modal-close-button');
    editModal.appendChild(modalCloseButtonDiv);

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    modalCloseButtonDiv.appendChild(closeBtn);

    // MODAL CONTENT
    const modalContent = document.createElement('div');
    modalContent.classList.add('edit-modal-content');
    editModal.appendChild(modalContent);

    // MODAL HEADER
    const modalHeader = document.createElement('div');
    modalHeader.classList.add('row', 'edit-modal-header');
    modalHeader.innerText = 'Edit Snippet:';
    modalContent.appendChild(modalHeader);

    //TITLE PARENT
    const modalTitleDiv = document.createElement('div');
    modalTitleDiv.classList.add('row');
    modalContent.appendChild(modalTitleDiv);

    //CLASSIFICATION PARENT
    const classificationCol = document.createElement('div');
    classificationCol.classList.add('col-fit');

    //CLASSIFICATION LABEL
    const classificationLabelRow = document.createElement('div');
    classificationLabelRow.classList.add('row', 'edit-title-label-row');

    const classificationLabel = document.createElement('span');
    classificationLabel.classList.add('edit-title-label');
    classificationLabel.innerText = 'Language: ';
    classificationLabelRow.appendChild(classificationLabel);
    classificationCol.appendChild(classificationLabelRow);

    //CLASSIFCATION INPUT
    const classificationSelectRow = document.createElement('div');
    classificationSelectRow.classList.add('row', 'edit-title-label-row');

    const snippetClassification = document.createElement('select');
    snippetClassification.classList.add('jp-dropdown', 'edit-dropdown');
    for (const [key, value] of Object.entries(
        ClassificationSpecificEnum
    ).sort()) {
        if (value === 'txt' || value === 'yml') continue;
        const readable = langExtToReadable(value);
        if (!readable) continue;
        const langOption = document.createElement('option');
        langOption.innerText = readable;
        langOption.value = key;
        snippetClassification.appendChild(langOption);
    }

    const curClassification = Object.keys(ClassificationSpecificEnum).find(
        (value) =>
            ClassificationSpecificEnum[
                value as keyof typeof ClassificationSpecificEnum
            ] === snippet.language
    );

    snippetClassification.value =
        curClassification ?? ClassificationSpecificEnum.Dart;

    snippetClassification.addEventListener('change', () => {
        editedContent.language =
            ClassificationSpecificEnum[
                snippetClassification.value as keyof typeof ClassificationSpecificEnum
            ];
    });

    classificationSelectRow.appendChild(snippetClassification);
    classificationCol.appendChild(classificationSelectRow);
    modalTitleDiv.appendChild(classificationCol);

    //TITLE LABEL
    const titleCol = document.createElement('div');
    titleCol.classList.add('col');

    const titleLabelRow = document.createElement('div');
    titleLabelRow.classList.add('row');
    titleCol.appendChild(titleLabelRow);
    const titleLabel = document.createElement('span');
    titleLabel.classList.add('edit-title-label');
    titleLabel.innerText = 'Title:';
    titleLabelRow.appendChild(titleLabel);

    //TITLE INPUT
    const titleInputRow = document.createElement('div');
    titleInputRow.classList.add('row', 'edit-title-label-row');
    const snippetTitle = document.createElement('input');
    snippetTitle.type = 'text';
    snippetTitle.classList.add('jp-input', 'edit-title-input');
    snippetTitle.value = snippet.title;
    snippetTitle.addEventListener('change', () => {
        editedContent.title = snippetTitle.value;
    });
    titleInputRow.appendChild(snippetTitle);
    titleCol.appendChild(titleInputRow);
    modalTitleDiv.appendChild(titleCol);

    //SNIPPET CODE
    const snippetDivOutter = document.createElement('div');
    snippetDivOutter.classList.add('row', 'snippet');
    snippetDivOutter.id = `snippet-${snippet.id}`;

    const snippetDiv = document.createElement('div');
    snippetDiv.classList.add('snippet-parent', 'row');
    snippetDiv.id = 'edit-snippet-parent';

    snippetDivOutter.appendChild(snippetDiv);
    let highlighted = highlightSnippet({
        snippetContent: snippet.raw,
        snippetLanguage: snippet.language,
    });

    const lineNumDiv = document.createElement('div');
    lineNumDiv.classList.add('snippet-line-div');
    snippetDiv.appendChild(lineNumDiv);

    const rawCodeDiv = document.createElement('div');
    rawCodeDiv.classList.add('snippet-raw');
    snippetDiv.appendChild(rawCodeDiv);
    const preElement = document.createElement('pre');
    preElement.classList.add('edit-snippet-raw-pre');
    rawCodeDiv.appendChild(preElement);

    const seperatedRaw = snippet.raw.split('\n');

    for (let i = 0; i < seperatedRaw.length; i++) {
        const lineNum = document.createElement('code');
        lineNum.classList.add('snippet-line-nums');
        lineNum.innerText = `${i + 1}`;
        lineNumDiv.appendChild(lineNum);
        const br = document.createElement('br');
        lineNumDiv.appendChild(br);
    }

    preElement.innerHTML = highlighted;

    modalContent.appendChild(snippetDivOutter);

    //SNIPPET DESCRIPTION
    const descRow = document.createElement('div');
    descRow.classList.add('row', 'edit-desc-row');

    const descEl = document.createElement('textarea');
    descEl.classList.add('jp-textarea', 'edit-desc-col');
    descEl.rows = 10;
    descEl.cols = 50;
    descEl.value = snippet.description || 'Unable to parse description';
    descEl.addEventListener('change', () => {
        editedContent.description = descEl.value;
    });
    descRow.appendChild(descEl);
    modalContent.appendChild(descRow);

    //SAVE BUTTON
    const btnRow = document.createElement('div');
    btnRow.classList.add('row', 'edit-desc-row');
    const saveBtn = document.createElement('button');
    saveBtn.classList.add('jp-btn');

    saveBtn.addEventListener('click', () => {
        modalContainer.remove();
        updateHandler(editedContent);
    });

    saveBtn.innerText = 'Save Changes';
    saveBtn.title = 'Save Changes';
    btnRow.appendChild(saveBtn);
    modalContent.appendChild(btnRow);

    //APPEND MODAL TO ROOT
    modalContainer.appendChild(modalBackground);
    modalContainer.appendChild(editModal);
    main!.appendChild(modalContainer);

    //MODAL CLOSE HANDLERS
    let clicks = 0;
    const handleWindowHide = (event: any) => {
        if (event.target !== editModal && !editModal.contains(event.target)) {
            clicks++;
            if (clicks >= 2) {
                window.removeEventListener('click', handleWindowHide);
                modalContainer.remove();
            }
        }
    };

    window.addEventListener('click', handleWindowHide);

    closeBtn.addEventListener('click', () => {
        modalContainer.remove();
    });
}

async function updateHandler(editedContent: {
    id: string;
    description: string;
    language: ClassificationSpecificEnum;
    title: string;
}): Promise<void> {
    try {
        const config = ConnectorSingleton.getInstance();
        let asset = await config.assetApi.assetSnapshot({
            asset: editedContent.id,
            transferables: false,
        });
        const originalClassification =
            asset.original?.reference?.classification.specific ??
            ClassificationSpecificEnum.Dart;

        // Update transaction
        if (editedContent.language !== originalClassification) {
            const newClassification = editedContent.language;

            asset =
                (await reclassify({
                    asset: asset,
                    ext: newClassification,
                })) || asset;
        }
        if (
            asset.name !== editedContent.title ||
            asset.description !== editedContent.description
        ) {
            asset.name = editedContent.title;
            asset.description = editedContent.description;

            asset = (await update({ asset: asset })) || asset;
        }
        // End update transaction
    } catch (error) {
        notifications.error({
            message: 'Failed to edit snippet, are you sure POS is running?',
        });
        console.log(error);
    }
}
