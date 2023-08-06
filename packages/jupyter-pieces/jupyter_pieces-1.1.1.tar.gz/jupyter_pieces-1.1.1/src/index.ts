import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { showOnboarding } from './onboarding/showOnboarding';
import { PiecesView } from './ui/piecesView';
import '../style/icons.css';
import '../style/prism.css';
import '../style/images.css';
import { getStored, setStored } from './localStorageManager';
import { createCommands } from './actions/create_commands';
import * as Sentry from '@sentry/browser';
import { SentryTracking } from './analytics/SentryTracking';
import {
    CapabilitiesEnum,
    ClassificationSpecificEnum,
    ConfigurationParameters,
    IntentionRequest,
    SuggestRequest,
} from './PiecesSDK/connector';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import ConnectorSingleton from './connection/connector_singleton';
import { SegmentAnalytics } from './analytics/SegmentAnalytics';
import { Heartbeat, pluginActivityCheck } from './analytics/Heartbeat';
import { IStateDB } from '@jupyterlab/statedb';
import PiecesCacheSingleton from './cache/pieces_cache';
import { Asset } from './PiecesSDK/core';
import { stream } from './connection/stream_assets';
import CheckVersionAndConnection from './connection/checkVersionAndConnection';
import { loadConnect } from './connection/api_wrapper';
import {
    drawSnippets,
    isLoading,
    setIsLoading,
    setIsFetchFailed,
} from './ui/views/create_snippet_view';
import { redrawGpt } from './ui/views/create_gpt_view';
import versionCheck from './connection/version_check';

/**
 * Initialization data for the jupyter-pieces extension.
 */
export const PLUGIN_ID = 'jupyter-pieces';
export let defaultApp: JupyterFrontEnd;
export let defaultView: PiecesView;
export let theme: string;
export let defaultState: IStateDB;
const cache = PiecesCacheSingleton.getInstance();
const config: ConnectorSingleton = ConnectorSingleton.getInstance();

export const pluginHeartbeat = new Heartbeat(5); // 5 minutes

const plugin: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID + ':plugin',
    description:
        'Pieces for Developers is a code snippet management tool powered by AI.',
    autoStart: true,
    requires: [ICommandPalette, IStateDB],
    optional: [],
    deactivate: async () => {
        await Sentry.close(2000);
        pluginHeartbeat.stop();
    },
    activate: async (
        app: JupyterFrontEnd,
        palette: ICommandPalette,
        state: IStateDB
    ) => {
        await versionCheck({ notify: true }); // Check for minimum version of POS

        theme = '';
        defaultApp = app;
        const piecesView = new PiecesView();
        defaultView = piecesView;
        await piecesView.build(app);
        loadConnect()
            .then((val) => {
                setIsFetchFailed(!val);
                drawSnippets({});
                document.getElementById('gpt-tab') ? redrawGpt() : '';
            })
            .catch(() => {
                // do nothing
            });
        createCommands({ palette });

        SentryTracking.init();
        SegmentAnalytics.init();

        pluginHeartbeat.start(() => {
            pluginActivityCheck();
        });
        app.restored
            .then(async () => {
                defaultState = state;
                const assets = (await state.fetch(
                    PLUGIN_ID
                )) as unknown as Asset[];
                if (!isLoading) {
                    return;
                }
                assets.forEach(
                    (val) => (val.created.value = new Date(val.created.value))
                );
                cache.store({ assets: assets as unknown as Asset[] });
            })
            .finally(async () => {
                CheckVersionAndConnection.run().then(() => {
                    stream();
                });
                if (!getStored('onBoardingShown')) {
                    showOnboarding();
                    setStored({ onBoardingShown: true });
                }
                setIsLoading(false);
                drawSnippets({});
            });

        document.body.addEventListener('click', () => {
            if (theme !== document.body.getAttribute('data-jp-theme-light')) {
                theme = document.body.getAttribute('data-jp-theme-light')!;
                drawSnippets({});
            }
        });

        document.addEventListener('copy', (e) => {
            const selection = window.getSelection()?.toString();
            if (selection) {
                const intention: IntentionRequest = {
                    application: config.context.application.id,
                    seededConnectorAsset: {
                        format: {
                            fragment: {
                                string: {
                                    raw: selection,
                                },
                                metadata: {
                                    ext: ClassificationSpecificEnum.Py,
                                },
                            },
                        },
                    },
                };
                try {
                    config.api.intention(intention);
                } catch (e) {
                    console.log('Pieces: Intent error', e);
                }
            }
        });

        document.addEventListener('paste', (e) => {
            const clipboard = e.clipboardData;
            if (clipboard) {
                const clipboardData = clipboard.getData('text/plain');
                const suggestion: SuggestRequest = {
                    application: config.context.application.id,
                    seededConnectorCreation: {
                        asset: {
                            format: {
                                fragment: {
                                    string: {
                                        raw: clipboardData,
                                    },
                                },
                            },
                        },
                    },
                };
                try {
                    config.api.suggest(suggestion);
                } catch (e) {
                    //
                }
            }
        });
    },
};

// Getting rid of stupid TS squiggles that aren't actually issues
const settings: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID + ':pieces-settings',
    description:
        'Pieces for Developers is a code snippet management tool powered by AI.',
    autoStart: true,
    requires: [ISettingRegistry],
    optional: [],
    activate: async (app: JupyterFrontEnd, settings: ISettingRegistry) => {
        const config: ConnectorSingleton = ConnectorSingleton.getInstance();
        function loadSetting(settings: ISettingRegistry.ISettings): void {
            // Read the settings and convert to the correct type
            if (
                getStored('AutoOpen') !==
                (settings.get('AutoOpen').composite as boolean)
            ) {
                setStored({
                    AutoOpen: settings.get('AutoOpen').composite as boolean,
                });
            }

            if (
                getStored('Port') !== (settings.get('Port').composite as number)
            ) {
                setStored({
                    Port: settings.get('Port').composite as number,
                });
                const ConfigParams: ConfigurationParameters = {
                    basePath: `http://localhost:${
                        settings.get('Port').composite as number
                    }`,
                    fetchApi: fetch,
                };
                config.parameters = ConfigParams;
            }

            if (
                getStored('Capabilities') !==
                (settings.get('Capabilities').composite as string).toUpperCase()
            ) {
                switch (settings.get('Capabilities').composite as string) {
                    case 'Local':
                        setStored({
                            Capabilities: CapabilitiesEnum.Local,
                        });
                        break;
                    case 'Blended':
                        setStored({
                            Capabilities: CapabilitiesEnum.Blended,
                        });
                        break;
                    case 'Cloud':
                        setStored({
                            Capabilities: CapabilitiesEnum.Cloud,
                        });
                        break;
                    default:
                        setStored({
                            Capabilities: CapabilitiesEnum.Blended,
                        });
                        break;
                }
                config.application.capabilities = getStored('Capabilities');
            }
        }

        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([
            app.restored,
            settings.load(PLUGIN_ID + ':pieces-settings'),
        ])
            .then(([, settings]) => {
                // Read the settings
                if (settings) {
                    loadSetting(settings);
                }

                // Listen for your plugin setting changes using Signal
                settings.changed.connect(loadSetting);
            })
            .catch((reason) => {
                console.error(
                    `Something went wrong when reading the settings.\n${reason}`
                );
            });
    },
};

export default [settings, plugin];
