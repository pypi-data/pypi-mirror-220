import ConnectorSingleton from '../connection/connector_singleton';
import {
    QGPTConversationMessage,
    QGPTQuestionAnswer,
    RelevanceRequest,
    RelevantQGPTSeeds,
    Seed,
    SeededFile,
    SeededFragment,
    SeedTypeEnum,
} from '../PiecesSDK/core';
import langExtToClassificationSpecificEnum from '../ui/utils/langExtToClassificationSpecificEnum';
import { defaultApp } from '..';
import { Contents, ContentsManager } from '@jupyterlab/services';
import { SHA256 } from 'crypto-js';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';

// data structure to relate a seed to a path
const qGPTSeedToFile: Map<string, string> = new Map<string, string>();
const UNIQUE_ID_SUBSTR_LEN = 40;
let qGPTSeedCache: Array<Contents.IModel> = [];

// maps path to 'last_modified' date string to make sure we don't fetch the same file twice
const fileLastModified: Map<string, string> = new Map<string, string>();

export const getSeedPath = (seed: Seed) => {
    return qGPTSeedToFile.get(
        generateUniqueId(
            seed.asset?.format?.fragment?.string?.raw!.substring(
                UNIQUE_ID_SUBSTR_LEN
            )!
        )
    );
};

/*
    This function will recursively get all the notebook files starting at '/' aka the directory jupyterlab was initialized from
    - returns a promise array of all the notebooks
*/
const getAllNotebooks = async (): Promise<Array<Promise<Contents.IModel>>> => {
    try {
        const MAX_FETCH = 400; // sets an upper limit on number of fetches
        let totalFetches = 0;
        const MAX_BYTES = 10_000_000; // only let 10 mb of notebooks be fetched
        let totalBytes = 0;
        const notebookContents: Array<Promise<Contents.IModel>> = [];
        const contentsFetching: Array<Promise<void>> = [];

        // helper to get contents of a file, detect if it's a notebook or not, and fetch recursively or not according
        const findNotebooks = async (file: Promise<Contents.IModel>) => {
            if (totalFetches > MAX_FETCH || totalBytes > MAX_BYTES) return;
            const fileContent = await file;
            // dont fetch a file if we already have it cached and it hasn't been modified
            if (
                fileLastModified.get(fileContent.path) &&
                fileLastModified.get(fileContent.path) ===
                    fileContent.last_modified
            ) {
                return;
            }
            fileLastModified.set(fileContent.path, fileContent.last_modified);
            // the current file is a notebook
            if (fileContent.type === 'notebook') {
                totalFetches++;
                totalBytes += fileContent.size ?? 0;

                if (totalBytes < MAX_BYTES) {
                    notebookContents.push(
                        contentsManager.get(fileContent.path, { content: true })
                    );
                }
                // current file is a directory
            } else if (fileContent.type === 'directory') {
                for (let i = 0; i < fileContent.content.length; i++) {
                    if (totalFetches > MAX_FETCH || totalBytes > MAX_BYTES) {
                        return;
                    }
                    totalFetches++;
                    contentsFetching.push(
                        findNotebooks(
                            contentsManager.get(fileContent.content[i].path)
                        )
                    );
                }
            }
        };
        const contentsManager = new ContentsManager();
        await findNotebooks(contentsManager.get('/'));
        await Promise.all(contentsFetching);
        return notebookContents;
    } catch (e) {
        console.log(e);
    }
    return [];
};

const generateUniqueId = (input: string): string => {
    const hash = SHA256(input).toString();
    return hash;
};

/*
    Loads in the context from all the notebooks
    updates the mapping to relate a seed to a file
    sends request to /relevance question: true
*/
export const askQGPT = async ({ query }: { query: string }) => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_QUESTION_ASKED,
    });

    const config = ConnectorSingleton.getInstance();
    const allNotebooks = [
        ...qGPTSeedCache,
        ...(await Promise.all(await getAllNotebooks())),
    ];
    qGPTSeedCache = allNotebooks;

    const relevanceParams: RelevanceRequest = {
        qGPTRelevanceInput: {
            query,
            seeds: {
                iterable: [],
            },
            options: {
                question: true,
            },
        },
    };

    for (let i = 0; i < allNotebooks.length; i++) {
        const cells = allNotebooks[i].content.cells;
        for (let j = 0; j < cells.length; j++) {
            if (!(cells[j].cell_type === 'code')) {
                continue;
            }
            const raw = cells[j].source;
            if (!raw) {
                continue;
            }
            const lang =
                //@ts-ignore 'kernelPreference' is not available from the ts api given by jupyterlab, however it does exist if the user has a notebook open
                // this is okay because we fallback to python if kernelPreference is undefined
                defaultApp.shell.currentWidget?.sessionContext?.kernelPreference
                    ?.language ?? 'py';

            let currentSeed: Seed = {
                type: SeedTypeEnum.Asset,
            };

            qGPTSeedToFile.set(
                generateUniqueId(raw.substring(UNIQUE_ID_SUBSTR_LEN)),
                allNotebooks[i].path
            );

            let seed: SeededFile | SeededFragment = {
                string: {
                    raw: raw,
                },
                metadata: {
                    ext: langExtToClassificationSpecificEnum(lang),
                },
            };

            currentSeed.asset = {
                application: config.context.application,
                format: {
                    fragment: seed,
                },
            };

            relevanceParams.qGPTRelevanceInput!.seeds!.iterable.push(
                currentSeed
            );
        }
    }

    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_QUESTION_SUCCESS,
    });

    return {
        result: await config.QGPTApi.relevance(relevanceParams),
        query: query,
    };
};

/*
    Generates a question to then pass to gpt
*/
export const reprompt = async ({
    conversation,
    query,
}: {
    conversation: QGPTConversationMessage[];
    query: string;
}) => {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_AI_ASSISTANT_REPROMPT,
    });

    const reversedConv = conversation.reverse();
    const config = ConnectorSingleton.getInstance();
    const repromptRes = await config.QGPTApi.reprompt({
        qGPTRepromptInput: {
            query: query,
            conversation: {
                iterable: reversedConv,
            },
        },
    });
    return askQGPT({ query: repromptRes.query });
};

/*
    Calls the hints api to generate hints based on the conversation
*/
export const hints = async ({
    relevant,
    answer,
    query,
}: {
    relevant: RelevantQGPTSeeds;
    answer?: QGPTQuestionAnswer;
    query?: string;
}) => {
    const config = ConnectorSingleton.getInstance();

    return config.QGPTApi.hints({
        qGPTHintsInput: {
            relevant,
            answer,
            query,
        },
    });
};
