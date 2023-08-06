import { PLUGIN_ID, defaultApp, defaultState } from '.';
import PiecesCacheSingleton from './cache/pieces_cache';
import { ReadonlyJSONObject } from '@lumino/coreutils';
import ConnectorSingleton from './connection/connector_singleton';
import { drawSnippets } from './ui/views/create_snippet_view';

export const timeoutPromise: (duration: number) => Promise<void> = (
    duration: number
): Promise<void> => new Promise((resolver) => setTimeout(resolver, duration));

export const PromiseResolution: {
    <T>(): {
        resolver: { (args: T): T | void };
        rejector: { (args: T): T | void };
        promise: Promise<T>;
    };
} = <T>() => {
    let resolver!: { (args: T): T | void };
    let rejector!: { (args: T): T | void };

    const promise: Promise<T> = new Promise<T>(
        (resolve: { (args: T): T | void }) => {
            resolver = (args: T) => resolve(args);
            rejector = (args: T) => resolve(args);
        }
    );
    return {
        promise,
        resolver,
        rejector,
    };
};

let writeId: NodeJS.Timeout;
export const writeDB = () => {
    clearTimeout(writeId);
    const cache = PiecesCacheSingleton.getInstance();
    writeId = setTimeout(async () => {
        defaultApp.restored.then(() => {
            defaultState.save(
                PLUGIN_ID,
                cache.assets as unknown as ReadonlyJSONObject
            );
        });
    }, 15_000);
};

export const clearStaleIds = async () => {
    const config = ConnectorSingleton.getInstance();
    const cache = PiecesCacheSingleton.getInstance();
    const idSnapshot = await config.assetsApi.assetsIdentifiersSnapshot();
    const idMap = new Map();
    idSnapshot.iterable?.forEach((identifier) => {
        idMap.set(identifier.id, true);
    });
    // if cache id is not in idsnapshot delete
    const staleIds = Object.keys(cache.mappedAssets).filter((id) => {
        return !idMap.has(id);
    });

    staleIds.forEach((id) => {
        const snippetEl = document.getElementById(`snippet-el-${id}`);
        snippetEl?.remove();
        delete cache.mappedAssets[id];
    });
    cache.assets = Object.values(cache.mappedAssets);
    writeDB();
    if (!cache.assets.length) {
        drawSnippets({});
    }
};
