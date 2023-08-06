import { LabIcon } from '@jupyterlab/ui-components';
import ConnectorSingleton from '../../connection/connector_singleton';
import Constants from '../../const';

let userSVG: LabIcon | HTMLImageElement;
const getProfile = async () => {
    if (userSVG) {
        return userSVG;
    }
    const config = ConnectorSingleton.getInstance();
    let user;
    try {
        user = (await config.userApi.userSnapshot()).user;
    } catch (e) {
        //
    }

    const profilePic = user?.picture;

    if (profilePic) {
        const img = new Image();
        img.src = profilePic;
        userSVG = img;
    } else {
        userSVG = new LabIcon({
            name: 'jupyter-pieces:userSVG',
            svgstr: Constants.USER_SVG,
        });
    }
    return userSVG;
};

export default getProfile;
