import Notifications from './notification_handler';
import ConnectorSingleton from './connector_singleton';
import Constants from '../const';
import { launchRuntime } from '../actions/launch_runtime';
import { gte, lt } from 'semver';

const notifications: Notifications = Notifications.getInstance();
const config: ConnectorSingleton = ConnectorSingleton.getInstance();
export const currentMinVersion = '5.1.2';
export const currentMaxVersion = '6.0.0';
export let versionValid = false;

/*
    Returns promise<true> if the user has a supported version of POS for this plugin
    otherwise... promise<false>
*/
export default async function versionCheck({
    retry,
    minVersion,
    notify = false,
}: {
    retry?: boolean;
    minVersion?: string;
    notify?: boolean;
}): Promise<boolean> {
    try {
        if (versionValid) {
            return versionValid;
        }
        const osVersion: string =
            await config.wellKnownApi.getWellKnownVersion();
        console.log('Pieces for Developers:  Pieces OS Version: ', osVersion);
        if (osVersion.includes('staging') || osVersion.includes('debug')) {
            versionValid = true;
            return true;
        }

        versionValid =
            gte(osVersion, minVersion ?? currentMinVersion) &&
            lt(osVersion, currentMaxVersion);

        if (!versionValid && notify) {
            notifications.error({ message: Constants.UPDATE_OS });
        }

        return versionValid;
    } catch (error: any) {
        if (retry) {
            console.log('retrying');
            return false;
        }
        if (error.code === 'ECONNREFUSED') {
            await launchRuntime(true);
        }
        return await versionCheck({ retry: true });
    }
}
