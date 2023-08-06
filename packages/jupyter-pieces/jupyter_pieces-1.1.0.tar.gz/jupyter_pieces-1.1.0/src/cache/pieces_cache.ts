import { Asset } from '../PiecesSDK/common';
import { SeededAsset } from '../PiecesSDK/common';
import { ClassificationSpecificEnum } from '../PiecesSDK/core';
import { FormatTransferable } from '../typedefs.d';

export default class PiecesCacheSingleton {
    private static _instance: PiecesCacheSingleton;
    public assets: Asset[] = [];
    public suggestedAssets: Asset[] = [];
    public explainedMappedAssets = new Map<string, SeededAsset>();
    public mappedAssets: { [key: string]: Asset } = {};
    public fetchedFormats: { [key: string]: Date } = {};

    public snippetMap = new Map<ClassificationSpecificEnum, string[]>();
    // this is a map of key: format uuid and value here is a transferable
    public formatTransferables: { [key: string]: FormatTransferable } = {};

    private constructor() {
        /* */
    }

    /**
     * Stores the loaded pieces in one singleton variable so they are accessible everywhere.
     */
    public store({
        assets: incomingAssets,
        transferables,
    }: {
        assets?: Asset[];
        transferables?: { [key: string]: FormatTransferable };
    }): void {
        if (incomingAssets) {
            this.assets = incomingAssets;
            this.convertToMap(incomingAssets);
        }
        if (transferables) {
            this.formatTransferables = transferables;
        }
    }
    /*
    This will add an asset to the beginning of the assets list
    @DEV make sure to provide transferables with the asset!!
  */
    public prependAsset({ asset }: { asset: Asset }): void {
        this.assets.unshift(asset);
        this.mappedAssets[asset.id] = asset;
        if (
            asset.original.reference?.file ||
            asset.original.reference?.fragment
        ) {
            this.formatTransferables[asset.original.reference?.id] = {
                file: asset.original.reference?.file,
                fragment: asset.original.reference?.fragment,
            };
        }
    }

    public updateAsset({ asset }: { asset: Asset }): void {
        for (let i = 0; i < this.assets.length; i++) {
            if (this.assets[i].id === asset.id) {
                this.assets[i] = asset;
            }
        }
        this.mappedAssets[asset.id] = asset;
    }

    /**
     * Maps the iterable of Pieces so they are accessible by the id.
     */
    public convertToMap(iterable: Asset[]): void {
        for (const iter of iterable) {
            this.mappedAssets[iter.id] = iter;
        }
    }

    /**
     *
     * Loads the scheme and providers for each piece required for the snippet display to work.
     */
    public static getInstance(): PiecesCacheSingleton {
        if (!PiecesCacheSingleton._instance) {
            PiecesCacheSingleton._instance = new PiecesCacheSingleton();
        }
        return PiecesCacheSingleton._instance;
    }
}
