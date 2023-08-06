import DeletePiece from '../actions/delete';

export default async function showDeleteModal(
    snippetID: string,
    snippetTitle: string
): Promise<void> {
    //ROOT DIV
    const main = document.getElementById('main');

    // MODAL CONTAINER
    const modalContainer = document.createElement('div');
    modalContainer.classList.add('edit-modal-container');

    // MODAL BACKGROUND
    const modalBackground = document.createElement('div');
    modalBackground.classList.add('edit-modal-background');

    //MODAL PARENT(S)
    const deleteModal = document.createElement('div');
    deleteModal.classList.add('edit-modal');

    //CLOSE BUTTON
    const modalCloseButtonDiv = document.createElement('div');
    modalCloseButtonDiv.classList.add('edit-modal-close-button');
    deleteModal.appendChild(modalCloseButtonDiv);

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    modalCloseButtonDiv.appendChild(closeBtn);

    // MODAL CONTENT
    const modalContent = document.createElement('div');
    modalContent.classList.add('edit-modal-content');
    deleteModal.appendChild(modalContent);

    // MODAL HEADER
    const modalHeader = document.createElement('div');
    modalHeader.classList.add('row', 'edit-modal-header', 'delete-modal-title');
    modalHeader.innerText = 'Delete piece: ';
    modalContent.appendChild(modalHeader);

    //TITLE PARENT
    const modalTitleDiv = document.createElement('div');
    modalTitleDiv.classList.add('row');
    modalContent.appendChild(modalTitleDiv);

    //TITLE LABEL
    const titleCol = document.createElement('div');
    titleCol.classList.add('col');

    const titleLabelRow = document.createElement('div');
    titleLabelRow.classList.add('row');
    titleCol.appendChild(titleLabelRow);
    const titleLabel = document.createElement('span');
    titleLabel.classList.add('delete-modal-label');
    titleLabel.innerText = `Are you sure you want to delete '${snippetTitle}'?`;
    titleLabelRow.appendChild(titleLabel);

    modalTitleDiv.appendChild(titleCol);

    //SAVE BUTTON
    const btnRow = document.createElement('div');
    btnRow.classList.add('row', 'delete-desc-row');
    const saveBtn = document.createElement('button');
    saveBtn.classList.add('jp-btn', 'delete-del-btn');

    saveBtn.addEventListener('click', () => {
        deleteHandler(snippetID);
        modalContainer.remove();
    });

    saveBtn.innerText = 'Delete';
    saveBtn.title = 'Delete piece';
    btnRow.appendChild(saveBtn);
    modalContent.appendChild(btnRow);

    //APPEND MODAL TO ROOT
    modalContainer.appendChild(modalBackground);
    modalContainer.appendChild(deleteModal);
    main!.appendChild(modalContainer);

    //MODAL CLOSE HANDLERS
    let clicks = 0;
    const handleWindowHide = (event: any) => {
        if (
            event.target !== deleteModal &&
            !deleteModal.contains(event.target)
        ) {
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

async function deleteHandler(snippetId: string): Promise<void> {
    try {
        await DeletePiece.delete({ id: snippetId });
        const snippetEl = document.getElementById(`snippet-el-${snippetId}`);
        snippetEl?.remove();
    } catch (error) {
        console.log(error);
    }
}
