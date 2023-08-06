import { returnedSnippet } from '../../typedefs';
import { highlightSnippet } from './../utils/loadPrism';
import copyToClipboard from './../utils/copyToClipboard';
import Notifications from '../../connection/notification_handler';
import Constants from '../../const';
import ShareableLinksService from '../../connection/shareable_link';
import { LabIcon } from '@jupyterlab/ui-components';
import showExportedSnippet from '../snippetExportView';
import showEditModal from '../editModal';
import createAsset from '../../actions/create_asset';
import showDeleteModal from '../deleteModal';
import { drawSnippets } from '../views/create_snippet_view';

const share: ShareableLinksService = ShareableLinksService.getInstance();
const notification: Notifications = Notifications.getInstance();
const copyIcon = new LabIcon({
    name: 'jupyter-pieces:copy',
    svgstr: Constants.COPY_SVG,
});
const shareIcon = new LabIcon({
    name: 'jupyter-pieces:share',
    svgstr: Constants.SHARE_SVG,
});
const deleteIcon = new LabIcon({
    name: 'jupyter-pieces:delete',
    svgstr: Constants.DELETE_SVG,
});
const expandIcon = new LabIcon({
    name: 'jupyter-pieces:expand',
    svgstr: Constants.EXPAND_SVG,
});
const editIcon = new LabIcon({
    name: 'jupyter-pieces:edit',
    svgstr: Constants.EDIT_SVG,
});
const saveIcon = new LabIcon({
    name: 'jupyter-pieces:save',
    svgstr: Constants.SAVE_SVG,
});

export function renderLoading(
    contentEl: Document,
    location = ''
): HTMLDivElement {
    const loading = contentEl.createElement('div');
    loading.classList.add(`${location}bouncing-loader`);
    const loading1 = contentEl.createElement('div');
    const loading2 = contentEl.createElement('div');
    const loading3 = contentEl.createElement('div');

    loading.appendChild(loading1);
    loading.appendChild(loading2);
    loading.appendChild(loading3);

    return loading;
}

export function renderSnippet(
    snippetData: returnedSnippet,
    isPreview: boolean = false
): HTMLDivElement {
    const snippet = document.createElement('div');
    snippet.id = `snippet-${snippetData.id}`;
    snippet.classList.add('snippet');

    const snippetDiv = document.createElement('div');
    snippetDiv.classList.add('snippet-parent', 'row');

    snippet.appendChild(snippetDiv);

    if (!isPreview) {
        const expandBtn = document.createElement('button');
        expandIcon.element({ container: expandBtn });
        expandBtn.title = 'Expand code snippet';
        expandBtn.classList.add('jp-btn-transparent');
        expandBtn.addEventListener('click', () => {
            showExportedSnippet({
                snippetData: snippetData,
            }).catch(() => {
                notification.error({
                    message:
                        'Failed to expand snippet, are you sure POS is running?',
                });
            });
        });
        snippetDiv.appendChild(expandBtn);
    }

    const lineNumDiv = document.createElement('div');
    lineNumDiv.classList.add('snippet-line-div');
    snippetDiv.appendChild(lineNumDiv);

    const rawCodeDiv = document.createElement('div');
    rawCodeDiv.classList.add('snippet-raw');
    snippetDiv.appendChild(rawCodeDiv);
    const preElement = document.createElement('pre');
    preElement.classList.add('snippet-raw-pre');
    if (isPreview) {
        preElement.style.marginLeft = '18px';
    }
    rawCodeDiv.appendChild(preElement);

    const seperatedRaw = snippetData.raw.split('\n');

    for (let i = 0; i < seperatedRaw.length; i++) {
        const lineNum = document.createElement('code');
        lineNum.classList.add('snippet-line-nums');
        lineNum.innerText = `${i + 1}`;
        lineNumDiv.appendChild(lineNum);
        const br = document.createElement('br');
        lineNumDiv.appendChild(br);
    }

    preElement.innerHTML = highlightSnippet({
        snippetContent: snippetData.raw,
        snippetLanguage: snippetData.language,
    });

    const snippetFooter = document.createElement('div');
    snippetFooter.classList.add('snippet-footer', 'row');

    //BUTTONS
    const btnRow = document.createElement('div');
    btnRow.id = `btn-${snippetData.id}`;
    btnRow.classList.add('snippet-btn-row');
    snippetFooter.appendChild(btnRow);

    const userBtnDiv = document.createElement('div');
    userBtnDiv.classList.add('snippet-btn-row-user');
    btnRow.appendChild(userBtnDiv);

    const verticalBreak = document.createElement('div');
    verticalBreak.classList.add('vert-break');

    if (isPreview) {
        //Add a save button
        const saveBtn = document.createElement('button');
        saveBtn.classList.add('jp-btn');
        saveBtn.title = 'Save snippet to Pieces';
        saveIcon.element({ container: saveBtn });
        saveBtn.addEventListener('click', async () => {
            const loading = renderLoading(document);
            userBtnDiv.replaceChild(loading, saveBtn);
            try {
                await createAsset(
                    snippetData.raw,
                    false,
                    snippetData.description
                );
            } catch (e) {
                console.log(e);
            }
            drawSnippets({});
            userBtnDiv.replaceChild(saveBtn, loading);
        });

        userBtnDiv.appendChild(saveBtn);
        userBtnDiv.appendChild(verticalBreak.cloneNode(true));
    }

    const copyBtn = document.createElement('button');
    copyBtn.classList.add('jp-btn');
    copyBtn.title = 'Copy snippet to clipboard';
    copyIcon.element({ container: copyBtn });
    copyBtn.addEventListener('click', async () => {
        await copyToClipboard(snippetData.raw);
        notification.information({
            message: Constants.COPY_SUCCESS,
        });
    });

    userBtnDiv.appendChild(copyBtn);
    userBtnDiv.appendChild(verticalBreak.cloneNode(true));

    if (!isPreview) {
        const shareBtn = document.createElement('button');
        shareBtn.classList.add('jp-btn');
        shareBtn.title = `Copy snippet's shareable link`;
        shareIcon.element({ container: shareBtn });
        shareBtn.addEventListener('click', async () => {
            const loading = renderLoading(document);
            userBtnDiv.replaceChild(loading, shareBtn);
            try {
                const link =
                    snippetData.share ??
                    (await share.generate({
                        id: snippetData.id,
                    }));
                await copyToClipboard(link ?? '');

                if (snippetData.share) {
                    notification.information({
                        message: Constants.LINK_GEN_COPY,
                    });
                }
            } catch (e) {
                console.log(e);
            }
            userBtnDiv.replaceChild(shareBtn, loading);
        });
        userBtnDiv.appendChild(shareBtn);
        userBtnDiv.appendChild(verticalBreak.cloneNode(true));
    }

    if (!isPreview) {
        const editBtn = document.createElement('button');
        editBtn.classList.add('jp-btn');
        editBtn.title = 'Edit snippet';
        editIcon.element({ container: editBtn });
        editBtn.addEventListener('click', async () => {
            showEditModal(snippetData);
        });
        userBtnDiv.appendChild(editBtn);
    }

    userBtnDiv.appendChild(verticalBreak.cloneNode(true));

    if (!isPreview) {
        //Add a delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.classList.add('jp-btn', 'delete-btn');
        deleteBtn.title = 'Delete snippet';
        deleteIcon.element({ container: deleteBtn });
        deleteBtn.addEventListener('click', async () => {
            showDeleteModal(snippetData.id, snippetData.title);
        });

        btnRow.appendChild(deleteBtn);
    }

    snippet.appendChild(snippetFooter);
    return snippet;
}
