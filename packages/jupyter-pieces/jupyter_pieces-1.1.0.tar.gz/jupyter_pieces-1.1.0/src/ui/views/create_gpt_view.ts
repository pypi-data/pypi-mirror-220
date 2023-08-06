import {
    QGPTRelevanceOutput,
    QGPTQuestionOutput,
    RelevantQGPTSeed,
} from '../../PiecesSDK/core';
import { askQGPT, getSeedPath, hints, reprompt } from '../../actions/qgpt';
import { QGPTConversationMessage } from '../../PiecesSDK/common/models/QGPTConversationMessage';
import { QGPTConversationMessageRoleEnum } from '../../PiecesSDK/common/models/QGPTConversationMessageRoleEnum';
import Notifications from '../../connection/notification_handler';
import { marked } from 'marked';
import {
    LabIcon,
    copyIcon,
    saveIcon,
    shareIcon,
} from '@jupyterlab/ui-components';
import Constants from '../../const';
import { highlightSnippet } from '../utils/loadPrism';
import langReadableToExt from '../utils/langReadableToExt';
import { defaultApp, theme } from '../..';
import copyToClipboard from '../utils/copyToClipboard';
import { findSimilarity } from '../../actions/create_commands';
import createAsset from '../../actions/create_asset';
import ShareableLinksService from '../../connection/shareable_link';
import { SegmentAnalytics } from '../../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../../analytics/AnalyticsEnum';
import { isFetchFailed } from './create_snippet_view';
import { versionValid } from '../../connection/version_check';
import getProfile from '../utils/getUserIcon';

let currentConversation: QGPTConversationMessage[] = [];
const notification: Notifications = Notifications.getInstance();
const shareableLinks: ShareableLinksService =
    ShareableLinksService.getInstance();
let tempCollapseTimer: NodeJS.Timeout | undefined = undefined; // Timer for the collapse button
let userSVG: LabIcon | HTMLImageElement;
let cancelled = true;
let parentContainer: HTMLDivElement;

let conversationArray: Array<{
    query: string;
    answer: string;
}> = [];

let generatingResults = false;

const sendSVG = new LabIcon({
    name: 'jupyter-pieces:sendSVG',
    svgstr: Constants.SEND_SVG,
});
const aiSVG = LabIcon.resolve({ icon: 'jupyter-pieces:aiSVG' });
const copilotWhite = new LabIcon({
    name: 'jupyter-pieces:copilotWhite',
    svgstr: Constants.COPILOT_WHITE,
});

const copilotBlack = new LabIcon({
    name: 'jupyter-pieces:copilotWhite',
    svgstr: Constants.COPILOT_BLACK,
});

/*
    Creates the top level elements for the copilot view
    @param containervar: the container element
*/
export async function createGPTView({
    containerVar,
    newInstance = false,
}: {
    containerVar: HTMLDivElement;
    newInstance?: boolean;
}): Promise<void> {
    userSVG = await getProfile();
    parentContainer = containerVar;
    parentContainer.innerHTML = '';

    parentContainer.classList.add('gpt-container');

    // gpt container
    const containerDiv = document.createElement('div');
    parentContainer.appendChild(containerDiv);
    containerDiv.classList.add('gpt-col');

    // div for all messages
    const textDiv = document.createElement('div');
    containerDiv.appendChild(textDiv);
    textDiv.classList.add('gpt-row', 'gpt-text-div');

    const textContent = document.createElement('div');
    textDiv.appendChild(textContent);
    textContent.classList.add('gpt-col', 'gpt-text-content');

    let introText: HTMLDivElement;
    // if there is not a conversation loaded, show the preview
    if (currentConversation.length == 0 || newInstance) {
        currentConversation = [];
        conversationArray = [];
        textContent.style.display = 'none';
        introText = document.createElement('div');
        textDiv.appendChild(introText);
        introText.classList.add('gpt-text-intro', 'gpt-col');

        const imageHolder = document.createElement('div');
        imageHolder.classList.add('gpt-img-logo');

        theme === 'false'
            ? copilotBlack.element({ container: imageHolder })
            : copilotWhite.element({ container: imageHolder });

        introText.appendChild(imageHolder);

        const titleDiv = document.createElement('div');
        introText.appendChild(titleDiv);
        titleDiv.classList.add('gpt-row', 'gpt-text-intro-title-div');

        const introTextTitle = document.createElement('p');
        titleDiv.appendChild(introTextTitle);
        introTextTitle.classList.add(
            'gpt-text-intro-content',
            'gpt-text-intro-title'
        );
        introTextTitle.innerText = 'Copilot Chat';

        const introTextSub = document.createElement('p');
        introText.appendChild(introTextSub);
        introTextSub.classList.add('gpt-text-intro-content');
        introTextSub.innerText = !versionValid
            ? 'POS is not up-to-date, please update to use Copilot.'
            : isFetchFailed
            ? 'Error connecting to POS! To use Copilot, please make sure Pieces OS is installed updated, and running.'
            : 'Ask Copilot a question about your notebook(s)';
    }

    // div for relevant files
    const fileRow = document.createElement('div');
    textDiv.appendChild(fileRow);
    fileRow.classList.add('gpt-row');
    fileRow.id = 'gpt-files-container';

    // hint div
    const hintRow = document.createElement('div');
    textDiv.appendChild(hintRow);
    hintRow.classList.add('gpt-row');
    hintRow.id = 'gpt-hints-container';

    // clear chat button
    const cancelSpan = document.createElement('span');
    textDiv.appendChild(cancelSpan);
    cancelSpan.classList.add('gpt-cancel');
    cancelSpan.innerText = 'Clear Chat';

    // user input
    const textAreaDiv = document.createElement('div');
    textContent.appendChild(textAreaDiv);
    textAreaDiv.classList.add('gpt-col-reverse', 'gpt-text-area');

    cancelSpan.addEventListener('mouseup', async () => {
        cancelled = true;
        currentConversation = [];
        conversationArray = [];
        generatingResults = false;
        createGPTView({
            containerVar: parentContainer,
            newInstance: true,
        });

        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_RESET,
        });
    });

    // user input
    const inputDiv = document.createElement('div');
    containerDiv.appendChild(inputDiv);
    inputDiv.classList.add('gpt-row', 'gpt-input');

    const inputText = document.createElement('span');
    inputDiv.appendChild(inputText);
    inputText.title = !versionValid
        ? 'POS is not up-to-date, please update to use Copilot.'
        : isFetchFailed
        ? 'POS not detected, please launch POS to use Copilot.'
        : 'Ask a question about your notebook(s)';
    inputText.classList.add('gpt-input-textarea');
    inputText.contentEditable =
        !versionValid || isFetchFailed ? 'false' : 'true';
    inputText.spellcheck = true;

    // send button
    const sendDiv = document.createElement('div');
    inputDiv.appendChild(sendDiv);
    sendDiv.classList.add('gpt-img-small', 'gpt-col');
    sendSVG.element({ container: sendDiv });

    const sendSVGDiv = sendDiv.firstChild as HTMLElement;
    sendSVGDiv.classList.add('gpt-send-unactive');

    sendDiv.addEventListener('mouseup', async () => {
        if (inputText.innerText === '') {
            return;
        }
        cancelled = false;
        await handleChat({
            inputText,
            textAreaDiv,
            currentConversation,
            introText,
        });
    });

    inputText.addEventListener('keyup', async (evt) => {
        if (inputText.innerText !== '') {
            sendSVGDiv.classList.add('gpt-send-active');
            sendSVGDiv.classList.remove('gpt-send-unactive');
        } else {
            sendSVGDiv.classList.add('gpt-send-unactive');
            sendSVGDiv.classList.remove('gpt-send-active');
        }
        if (evt.key !== 'Enter' || evt.shiftKey) {
            return;
        }
        if (inputText.innerText === '') {
            return;
        }
        sendSVGDiv.classList.remove('gpt-send-active');
        sendSVGDiv.classList.add('gpt-send-unactive');
        hintRow.innerHTML = '';
        cancelled = false;
        await handleChat({
            inputText,
            textAreaDiv,
            currentConversation,
            introText,
        });
    });

    if (conversationArray.length != 0 && !newInstance) {
        buildCurrentConversation(textAreaDiv);
    }
}

// const showGPTErrorView = () => {
//     const parent = document.getElementById('gpt-tab') as HTMLDivElement;
//     const errorRow = document.createElement('div');
//     errorRow.classList.add('gpt-row');
//     parent.appendChild(errorRow);
//     const errorText = document.createElement('p');
//     errorText.innerText = 'There was an issue connecting to POS';
//     errorRow.appendChild(errorText);
// };

export const redrawGpt = () => {
    const parent = document.getElementById('gpt-tab') as HTMLDivElement;
    if (!parent) {
        return;
    }
    cancelled = true;
    currentConversation = [];
    conversationArray = [];
    generatingResults = false;
    createGPTView({ containerVar: parent, newInstance: true });
};

const handleChat = async ({
    inputText,
    textAreaDiv,
    currentConversation,
    introText,
}: {
    inputText: HTMLSpanElement;
    textAreaDiv: HTMLDivElement;
    currentConversation: QGPTConversationMessage[];
    introText: HTMLDivElement;
}): Promise<void> => {
    // make sure they can't send a message while one is processing
    if (generatingResults) {
        Notifications.getInstance().error({
            message: 'Already generating a message! Please wait a bit.',
        });
        return;
    }

    // Remove / clear dom elements where necessary
    document.getElementById('gpt-files-container')!.innerHTML = '';
    generatingResults = true;
    if (currentConversation.length == 0) {
        textAreaDiv.innerHTML = '';
    }
    const curQuery = inputText.innerText.trim();
    inputText.innerText = '';
    if (curQuery == '') {
        generatingResults = false;
        return;
    }
    let result: QGPTRelevanceOutput;
    if (introText) {
        textAreaDiv.parentElement!.style.display = 'flex';
        introText.remove();
    }
    const queryDiv = document.createElement('div');
    queryDiv.classList.add('gpt-row', 'gpt-right-align');

    // build chat message dom elements
    const answerQuery = document.createElement('p');
    answerQuery.classList.add('gpt-text-response', 'gpt-query');
    answerQuery.innerText = curQuery;

    const userDiv = document.createElement('div');
    userDiv.id = 'user-img';
    if (userSVG instanceof HTMLImageElement) {
        userSVG.classList.add('gpt-user-image');
        userDiv.appendChild(userSVG.cloneNode(true));
    } else {
        userSVG.element({ container: userDiv });
    }
    userDiv.classList.add('gpt-img');

    queryDiv.appendChild(answerQuery);
    queryDiv.appendChild(userDiv);

    textAreaDiv.insertBefore(queryDiv, textAreaDiv.firstChild);

    const answerDiv = document.createElement('div');
    answerDiv.classList.add('gpt-row', 'gpt-left-align');

    const aiDiv = document.createElement('div');
    aiDiv.id = 'ai-img';
    aiSVG.element({ container: aiDiv });
    aiDiv.classList.add('gpt-img');
    answerDiv.appendChild(aiDiv);

    const answerEl = document.createElement('p');
    answerEl.classList.add('gpt-text-response', 'gpt-response', 'gpt-col');
    answerEl.innerText = "Let's see what I got here...";

    answerDiv.appendChild(answerEl);

    textAreaDiv.prepend(answerDiv);

    setTimeout(() => {
        if (answerEl.innerText == `Let's see what I got here...`) {
            answerEl.innerText = `Choosing the best answer for your question...`;
        }
    }, 2000);

    setTimeout(() => {
        if (
            answerEl.innerText ==
            `Choosing the best answer for your question...`
        ) {
            answerEl.innerText = `Almost there...`;
        }
    }, 10000);
    // call reprompt if it's the 2nd or later message
    try {
        if (currentConversation.length == 0 /* conversation is empty */) {
            const askResponse = await askQGPT({ query: curQuery });
            result = askResponse.result;
        } else {
            const repromptResponse = await reprompt({
                query: curQuery,
                conversation: currentConversation,
            });
            result = repromptResponse.result;
        }
    } catch (e) {
        console.error(e);
        answerEl.innerText = 'Sorry, something went wrong with that request.';
        generatingResults = false;
        return;
    }

    const answer = result.answer?.answers.iterable[0];
    const relevant = result.relevant;

    // if the chat was successful, udpate the currentconversation object
    // as well as render the suggested files + hints response
    if (answer) {
        currentConversation.push({
            text: curQuery,
            role: QGPTConversationMessageRoleEnum.User,
            // subtract 10 as arbitrary number to ensure sort validity
            timestamp: { value: new Date(new Date().getTime() - 10) },
        });

        currentConversation.push({
            text: answer.text,
            role: QGPTConversationMessageRoleEnum.Assistant,
            timestamp: { value: new Date() },
        });

        // convert gpt response markdown to html
        if (answer?.text) {
            answerEl.innerHTML = marked.parse(answer.text, {
                headerIds: false,
                mangle: false,
            });
        } else {
            answerEl.innerHTML = marked.parse(
                `I'm sorry, it seems I don't have any relevant context to that question. Please try again 😃`,
                { headerIds: false, mangle: false }
            );
        }

        if (relevant.iterable) {
            renderSuggestedFiles(relevant.iterable, answerEl);
            hints({
                query: curQuery,
                relevant: relevant,
                answer: answer,
            })
                .then((hintsRes) => {
                    if (cancelled || !hintsRes.answers.iterable.length) {
                        return;
                    } else {
                        renderHints({
                            hints: hintsRes,
                            inputText,
                            introText,
                            textAreaDiv,
                        });
                    }
                })
                .catch(() => {
                    // do nothing
                });
        }
    } else {
        answerEl.innerHTML = marked.parse(
            `I'm sorry, it seems I don't have any relevant context to that question. Please try again 😃`,
            { headerIds: false, mangle: false }
        );
    }

    const pChildren = Array.from((answerEl as HTMLParagraphElement).children);

    const codeChildren: HTMLElement[] = [];

    // find the <code> elements
    pChildren.forEach((child) => {
        child.classList.add('gpt-response-margin-delete');
        if (child.tagName.toUpperCase() === 'PRE') {
            child.classList.add('gpt-col');
            codeChildren.push(child.children[0] as HTMLElement);
            child.children[0].classList.add('code-element');
        }
    });

    // add syntax highlighting to the <code> elements
    // also add embedded buttons
    if (codeChildren.length) {
        codeChildren.forEach((codeChild) => {
            let lang: string;
            try {
                lang = (codeChild?.classList[0] as string).split('-')[1];
            } catch {
                lang = 'py';
            }

            codeChild.innerHTML = highlightSnippet({
                snippetContent: codeChild.innerText,
                snippetLanguage: langReadableToExt(lang),
            });

            const buttonDiv = buildButtonHolder(codeChild);

            codeChild.appendChild(buttonDiv);
        });
    }

    conversationArray.push({ query: curQuery, answer: answerEl.innerText });
    generatingResults = false;
};

/*
    Builds the conversation while switching back to copilot
     - textareadiv: the container for the chat messages
*/
const buildCurrentConversation = (textAreaDiv: HTMLDivElement) => {
    conversationArray.forEach((element) => {
        const queryDiv = document.createElement('div');
        queryDiv.classList.add('gpt-row', 'gpt-right-align');

        const answerQuery = document.createElement('p');
        queryDiv.appendChild(answerQuery);
        answerQuery.classList.add('gpt-text-response', 'gpt-query');
        answerQuery.innerText = element.query;

        const userDiv = document.createElement('div');
        queryDiv.appendChild(userDiv);
        userDiv.classList.add('gpt-img');

        textAreaDiv.prepend(queryDiv);

        const answerDiv = document.createElement('div');
        answerDiv.classList.add('gpt-row', 'gpt-left-align');

        const aiDiv = document.createElement('div');
        answerDiv.appendChild(aiDiv);
        aiDiv.classList.add('gpt-img');

        const answerEl = document.createElement('p');
        answerDiv.appendChild(answerEl);
        answerEl.classList.add('gpt-text-response', 'gpt-response', 'gpt-col');
        answerEl.innerText = element.answer;
        textAreaDiv.prepend(answerDiv);
    });
};

/*
    Renders the suggested query buttones
     - hints: response from /hints
     - inputtext: the user input div
     - textareadiv: the chat messages container
     - introText: the container for the introduction text (if there is not a conversation)
*/
const renderHints = ({
    hints,
    inputText,
    textAreaDiv,
    introText,
}: {
    hints: QGPTQuestionOutput;
    inputText: HTMLSpanElement;
    textAreaDiv: HTMLDivElement;
    introText: HTMLDivElement;
}) => {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const hintRow = document.getElementById('gpt-hints-container')!;
    hintRow.innerHTML = '';
    const hintCol = document.createElement('div');
    hintRow.appendChild(hintCol);
    hintCol.classList.add('gpt-col', 'hpt-hint-col');

    // setup container(s)
    const hintTitleRow = document.createElement('div');
    hintCol.appendChild(hintTitleRow);
    hintTitleRow.classList.add('gpt-row', 'gpt-hint-row');
    const hintTitle = document.createElement('p');
    hintTitle.innerText = 'Suggested Queries: ';
    hintTitleRow.appendChild(hintTitle);
    hintTitle.classList.add('hint-title', 'hint-title-file');

    const hintListRow = document.createElement('div');
    hintCol.appendChild(hintListRow);
    hintListRow.classList.add('gpt-row', 'hint-list');

    const hintList = document.createElement('div');
    hintListRow.appendChild(hintList);
    hintList.classList.add('gpt-col');

    // render the buttons for every hint
    for (let i = 0; i < hints.answers.iterable.length; i++) {
        if (cancelled) {
            createGPTView({
                containerVar: parentContainer,
                newInstance: true,
            });
        }
        const hintButton = document.createElement('button');
        hintList.appendChild(hintButton);
        hintButton.classList.add('hint-btn', 'gpt-row');
        hintButton.onclick = () => {
            hintRow.innerHTML = '';
            inputText.innerText = hints.answers.iterable[i].text;
            handleChat({
                inputText,
                textAreaDiv,
                currentConversation,
                introText,
            });

            SegmentAnalytics.track({
                event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_CLICKED_SUGGESTED_QUERY,
            });
        };

        const hintButtonText = document.createElement('p');
        hintButton.appendChild(hintButtonText);
        hintButtonText.classList.add('hint-btn-text', 'gpt-col');
        hintButtonText.textContent = hints.answers.iterable[i].text;

        // add icon to the button
        const sendIconDiv = document.createElement('div');
        sendIconDiv.classList.add('gpt-btn-icon');
        hintButton.appendChild(sendIconDiv);
        sendSVG.element({ container: sendIconDiv });
    }
};

// in the case that we get multiple relevant snippets from the same file,
// we need to remove the duplicate files from the rendered list
const deleteIdenticalElements = (
    files: RelevantQGPTSeed[]
): RelevantQGPTSeed[] => {
    const result: RelevantQGPTSeed[] = [];
    const paths: { [key: string]: boolean } = {};
    files.forEach((file: RelevantQGPTSeed) => {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        if (!paths[file.path!]) {
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            paths[file.path!] = true;
            result.push(file);
        }
    });
    return result;
};
// Renders suggested files to the dom
const renderSuggestedFiles = (
    files: RelevantQGPTSeed[],
    answerEl: HTMLDivElement
) => {
    // make sure there is no duplicates using a set also get all the paths from the map in qgpt.ts
    files = deleteIdenticalElements(files);

    if (files.length == 0) {
        return;
    }

    const filePaths: Set<string> = new Set<string>();
    for (let i = 0; i < files.length; i++) {
        const path = getSeedPath(files[i].seed!);
        if (path) filePaths.add(path);
    }

    const fileRow = answerEl;

    // button(s) container(s)
    const fileCol = document.createElement('div');
    fileRow.appendChild(fileCol);
    fileCol.classList.add('gpt-col');

    const fileTitleRow = document.createElement('div');
    fileCol.appendChild(fileTitleRow);
    fileTitleRow.classList.add('gpt-row');
    const fileTitle = document.createElement('p');
    fileTitle.textContent = 'Relevant Files: ';
    fileTitleRow.appendChild(fileTitle);
    fileTitle.classList.add('hint-title-file');

    const fileListRowDiv = document.createElement('div');
    fileCol.appendChild(fileListRowDiv);
    fileListRowDiv.classList.add('gpt-row', 'hint-list-file');

    const fileListCol = document.createElement('div');
    fileListRowDiv.appendChild(fileListCol);
    fileListCol.classList.add('gpt-col');

    const fileListRow = document.createElement('div');
    fileListCol.appendChild(fileListRow);
    fileListRow.classList.add('gpt-row', 'gpt-rel-wrap');

    // Create the file pills
    // 2 per row
    filePaths.forEach((path) => {
        createFilePill(path, fileListRow);
    });
};

// // DOM element for a file pill
// // file: the file to be rendered
// // fileListRow: the parent element
const createFilePill = (path: string, fileListRow: HTMLDivElement) => {
    const fileList = document.createElement('div');
    fileListRow.appendChild(fileList);
    fileList.classList.add('gpt-col-small');

    const fileName = (path?.substring(path.lastIndexOf('/') + 1) ?? '').split(
        '.'
    )[0];

    const fileButton = document.createElement('button');
    fileList.appendChild(fileButton);
    fileButton.title = `Open '${fileName}' in a new tab`;
    fileButton.classList.add('hint-btn-file');
    fileButton.onclick = () => {
        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_OPEN_RELEVANT_FILE,
        });

        defaultApp.commands.execute('docmanager:open', {
            path: path,
            options: {
                mode: 'tab-after',
            },
        });
    };

    const fileButtonText = document.createElement('p');
    fileButton.appendChild(fileButtonText);
    fileButtonText.classList.add('hint-btn-text', 'gpt-col');
    fileButtonText.textContent = path ?? '';

    const fileButtonIcon = document.createElement('div');
    fileButton.appendChild(fileButtonIcon);
    fileButtonIcon.classList.add('gpt-btn-icon', 'gpt-icon-file');
    const openFile = new LabIcon({
        name: 'jupyter-pieces:openFile',
        svgstr: Constants.OPEN_ICON,
    });
    openFile.element({ container: fileButtonIcon });
};

/*
    This is for our button holder
    in obsidian this is a widget class that also gets injected into the editor 
    but we declare it here because we don't inject anything

    snippetData is the <code> element that comes from gpt

*/
const buildButtonHolder = (snippetData: HTMLElement): HTMLDivElement => {
    const buttonDiv = document.createElement('div');
    buttonDiv.classList.add('gpt-response-button-div');

    const holderDiv = document.createElement('div');
    holderDiv.classList.add('save-to-pieces-holder');

    const collapsedHolder = document.createElement('div');
    collapsedHolder.classList.add('collapsed-pieces-holder', 'collapsed');

    const collapseControlButton = document.createElement('button');
    holderDiv.appendChild(collapseControlButton);
    collapseControlButton.title = 'See Pieces actions';
    collapseControlButton.classList.add('jp-btn');
    const piecesIcon = LabIcon.resolve({ icon: 'jupyter-pieces:logo' });
    piecesIcon.element({ container: collapseControlButton });
    collapseControlButton.addEventListener('click', async () => {
        clearTimeout(tempCollapseTimer);

        // detect if this exact code has been saved or not
        const { similarity, comparisonID } = await findSimilarity(
            snippetData.innerText
        );

        // if it's collapsed, render the buttons
        if (collapsedHolder.classList.contains('collapsed')) {
            const copyBtn = document.createElement('button');
            collapsedHolder.appendChild(copyBtn);
            copyBtn.classList.add('jp-btn', 'gpt-button-div');
            copyBtn.title = 'Copy snippet to clipboard';
            copyIcon.element({ container: copyBtn });
            copyBtn.addEventListener('click', async () => {
                await copyToClipboard(snippetData.innerText);
                notification.information({
                    message: Constants.COPY_SUCCESS,
                });
            });
            // if we don't have a similar snippet make it a save button
            if (similarity > 2) {
                const saveBtn = document.createElement('button');
                collapsedHolder.appendChild(saveBtn);
                saveBtn.classList.add('jp-btn', 'gpt-button-div');
                saveBtn.title = 'Save snippet to pieces';
                saveIcon.element({ container: saveBtn });
                saveBtn.addEventListener('click', async () => {
                    const loading = document.createElement('div');
                    loading.classList.add('share-code-bouncing-loader');
                    const bounceDiv = document.createElement('div');
                    loading.appendChild(bounceDiv);
                    loading.appendChild(bounceDiv.cloneNode(true));
                    loading.appendChild(bounceDiv.cloneNode(true));

                    collapsedHolder.replaceChild(loading, saveBtn);
                    await createAsset(snippetData.innerText, false, undefined);
                    collapsedHolder.removeChild(loading);
                    const computedWidth =
                        (5 + 42) * collapsedHolder.childElementCount;
                    collapsedHolder.style.width = computedWidth + 'px';
                });
            }

            // create share button
            const shareBtn = document.createElement('button');
            collapsedHolder.appendChild(shareBtn);
            shareBtn.classList.add('jp-btn', 'gpt-button-div');
            shareBtn.title = 'Copy snippet to clipboard';
            shareIcon.element({ container: shareBtn });
            shareBtn.addEventListener('click', async () => {
                const loading = document.createElement('div');
                loading.classList.add('share-code-bouncing-loader');
                const bounceDiv = document.createElement('div');
                loading.appendChild(bounceDiv);
                loading.appendChild(bounceDiv.cloneNode(true));
                loading.appendChild(bounceDiv.cloneNode(true));

                collapsedHolder.replaceChild(loading, shareBtn);

                // if it's already saved, use the existing snippet, otherwise save it as a new snippet
                if (similarity < 2 && comparisonID) {
                    const link = await shareableLinks.generate({
                        id: comparisonID,
                    });
                    copyToClipboard(link ?? '');
                } else {
                    const id = await createAsset(snippetData.innerText);
                    if (typeof id === 'string') {
                        const link = await shareableLinks.generate({
                            id: id,
                        });
                        copyToClipboard(link ?? '');
                    }
                }

                collapsedHolder.replaceChild(shareBtn, loading);
            });

            collapsedHolder.classList.remove('collapsed');
            const computedWidth = (3 + 42) * collapsedHolder.childElementCount;
            collapsedHolder.style.width = computedWidth + 'px';

            tempCollapseTimer = setTimeout(() => {
                tempCollapseTimer = undefined;
                collapsedHolder.classList.add('expanded');
            }, 500);

            collapseControlButton.title = 'Hide Pieces actions';
        } else {
            // the button is open, so collapse it
            collapsedHolder.classList.remove('expanded');
            collapsedHolder.classList.add('collapsed');
            collapsedHolder.style.width = '0px';
            collapseControlButton.disabled = true;
            tempCollapseTimer = setTimeout(() => {
                tempCollapseTimer = undefined;
                collapsedHolder.innerHTML = '';
                collapseControlButton.disabled = false;
            }, 500);

            collapseControlButton.title = 'See Pieces actions';
        }
    });

    holderDiv.appendChild(collapsedHolder);
    buttonDiv.appendChild(holderDiv);

    const children = Array.from(holderDiv.children);
    children.reverse();
    holderDiv.innerHTML = '';
    children.forEach((child) => holderDiv.appendChild(child));

    return buttonDiv;
};
