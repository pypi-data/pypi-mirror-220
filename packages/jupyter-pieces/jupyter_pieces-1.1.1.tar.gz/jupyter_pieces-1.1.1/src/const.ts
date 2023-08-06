import { AnalyticsEnum } from './analytics/AnalyticsEnum';

export default class Constants {
    public static PLUGIN_VERSION = '0.1.0';
    public static PIECES_USER_ID = '';
    public static PIECES_CURRENT_VIEW:
        | AnalyticsEnum.JUPYTER_VIEW_SNIPPET_LIST
        | AnalyticsEnum.JUPYTER_VIEW_CHATBOT =
        AnalyticsEnum.JUPYTER_VIEW_SNIPPET_LIST;

    public static readonly PIECES_LOGO = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20" height="20" viewBox="0 0 100 100" fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 41 1.601562 C 30.199219 4.601562 21.101562 12.101562 16.199219 22 L 13.5 27.5 L 13.199219 54.699219 L 12.898438 82 L 15.699219 87.199219 C 25.5 105.101562 51.101562 102.800781 57.300781 83.300781 C 58.199219 80.699219 59 77.398438 59.199219 76.101562 C 59.398438 74.398438 60.601562 73.300781 63.699219 72.101562 C 77.898438 66.601562 87 53.101562 87 37.5 C 87 28.699219 84.898438 22.398438 79.601562 15.199219 C 71.199219 3.699219 54.601562 -2.199219 41 1.601562 Z M 62.699219 11.800781 C 83.199219 22.300781 84.101562 51.5 64.199219 62.300781 L 59.199219 65 L 58.800781 52.5 C 58.398438 39 57.699219 37.101562 51.699219 32.601562 C 48 29.898438 40.199219 30 36.199219 32.898438 C 31.300781 36.300781 29.699219 41.101562 30.199219 50.398438 C 30.898438 62.898438 35.5 69.898438 45.601562 73.300781 C 48.800781 74.398438 49.5 75.199219 49.800781 77.601562 C 50.101562 81.300781 47 86.398438 42.800781 89.101562 C 40.300781 90.601562 38.300781 91 34.898438 90.699219 C 29.398438 90.199219 25.898438 87.898438 23 82.699219 C 20.898438 79 20.800781 78 21.199219 54.699219 C 21.5 31.699219 21.601562 30.300781 23.800781 25.800781 C 26.699219 20 34.601562 12.699219 40.300781 10.601562 C 46.199219 8.398438 57.199219 9 62.699219 11.800781 Z M 49 40.898438 C 50.101562 43.101562 50.398438 66 49.300781 66 C 47.5 66 42 61.898438 40.398438 59.5 C 38.199219 56.199219 37.800781 43.101562 39.898438 40.699219 C 41.800781 38.300781 47.699219 38.5 49 40.898438 Z M 49 40.898438 "/></svg>`;
    public static readonly PIECES_LOGO_ALT =
        'M 8.199219 0.320312 C 6.039062 0.921875 4.21875 2.421875 3.238281 4.398438 L 2.699219 5.5 L 2.640625 10.941406 L 2.578125 16.398438 L 3.140625 17.441406 C 5.101562 21.019531 10.21875 20.558594 11.460938 16.660156 C 11.640625 16.140625 11.800781 15.480469 11.839844 15.21875 C 11.878906 14.878906 12.121094 14.660156 12.738281 14.421875 C 15.578125 13.320312 17.398438 10.621094 17.398438 7.5 C 17.398438 5.738281 16.980469 4.480469 15.921875 3.039062 C 14.238281 0.738281 10.921875 -0.441406 8.199219 0.320312 Z M 12.539062 2.359375 C 16.640625 4.460938 16.820312 10.300781 12.839844 12.460938 L 11.839844 13 L 11.761719 10.5 C 11.679688 7.800781 11.539062 7.421875 10.339844 6.519531 C 9.601562 5.980469 8.039062 6 7.238281 6.578125 C 6.261719 7.261719 5.941406 8.21875 6.039062 10.078125 C 6.179688 12.578125 7.101562 13.980469 9.121094 14.660156 C 9.761719 14.878906 9.898438 15.039062 9.960938 15.519531 C 10.019531 16.261719 9.398438 17.28125 8.558594 17.820312 C 8.058594 18.121094 7.660156 18.199219 6.980469 18.140625 C 5.878906 18.039062 5.179688 17.578125 4.601562 16.539062 C 4.179688 15.800781 4.160156 15.601562 4.238281 10.941406 C 4.300781 6.339844 4.320312 6.058594 4.761719 5.160156 C 5.339844 4 6.921875 2.539062 8.058594 2.121094 C 9.238281 1.679688 11.441406 1.800781 12.539062 2.359375 Z M 9.800781 8.179688 C 10.019531 8.621094 10.078125 13.199219 9.859375 13.199219 C 9.5 13.199219 8.398438 12.378906 8.078125 11.898438 C 7.640625 11.238281 7.558594 8.621094 7.980469 8.140625 C 8.359375 7.660156 9.539062 7.699219 9.800781 8.179688 Z M 9.800781 8.179688';
    public static readonly REFRESH_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-refresh-cw"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>`;
    public static readonly CANCEL_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>`;
    public static readonly COPY_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`;
    public static readonly SHARE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-share-2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/></svg>`;
    public static readonly DELETE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash-2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>`;
    public static readonly EDIT_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-edit-3"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`;
    public static readonly EXPAND_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-expand"><path d="m21 21-6-6m6 6v-4.8m0 4.8h-4.8"/><path d="M3 16.2V21m0 0h4.8M3 21l6-6"/><path d="M21 7.8V3m0 0h-4.8M21 3l-6 6"/><path d="M3 7.8V3m0 0h4.8M3 3l6 6"/></svg>`;
    public static readonly SAVE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-save-all"><path d="M6 4a2 2 0 0 1 2-2h10l4 4v10.2a2 2 0 0 1-2 1.8H8a2 2 0 0 1-2-2Z"/><path d="M10 2v4h6"/><path d="M18 18v-7h-8v7"/><path d="M18 22H4a2 2 0 0 1-2-2V6"/></svg>`;
    public static readonly CODE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-braces"><path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/></svg>`;
    public static readonly AI_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="75" height="75" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot"><rect width="18" height="10" x="3" y="11" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" x2="8" y1="16" y2="16"/><line x1="16" x2="16" y1="16" y2="16"/></svg>`;
    public static readonly SEND_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-forward"><polyline points="15 17 20 12 15 7"/><path d="M4 18v-2a4 4 0 0 1 4-4h12"/></svg>`;
    public static readonly USER_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-circle-2"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg>`;
    public static readonly OPEN_ICON =
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-panel-right-open"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="15" x2="15" y1="3" y2="21"/><path d="m10 15-3-3 3-3"/></svg>';
    public static readonly COPILOT_WHITE = `<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
     "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
     width="512.000000pt" height="178.000000pt" viewBox="0 0 512.000000 178.000000"
     preserveAspectRatio="xMidYMid meet">
    
    <g transform="translate(0.000000,178.000000) scale(0.100000,-0.100000)"
    fill="#000000" stroke="none">
    <path d="M727 1765 c-178 -34 -329 -115 -463 -249 -212 -212 -300 -488 -249
    -781 32 -185 107 -326 245 -466 188 -190 418 -280 675 -266 226 13 407 91 569
    246 119 114 193 236 243 398 24 80 27 102 27 243 -1 139 -3 164 -27 243 -50
    162 -124 284 -243 398 -118 112 -239 180 -389 219 -106 28 -283 35 -388 15z
    m306 -276 c194 -65 327 -246 327 -444 0 -190 -129 -372 -311 -440 l-46 -17 -6
    -58 c-6 -68 -45 -148 -92 -187 -16 -15 -54 -37 -84 -51 -45 -21 -64 -24 -125
    -20 -114 8 -204 68 -250 167 -20 43 -21 65 -24 344 -2 189 1 318 8 351 35 170
    173 317 340 362 73 20 192 17 263 -7z"/>
    <path d="M785 1390 c-58 -18 -140 -76 -177 -125 -70 -92 -73 -112 -73 -456 l0
    -305 27 -41 c47 -72 138 -100 215 -68 50 21 72 42 94 90 28 60 25 93 -8 101
    -93 22 -179 98 -207 182 -20 58 -21 220 -2 265 42 103 183 140 272 72 61 -47
    74 -89 74 -252 0 -79 2 -143 5 -143 3 0 27 11 53 24 64 33 125 99 159 171 24
    51 28 72 28 145 -1 70 -5 94 -27 140 -36 78 -86 131 -160 170 -56 31 -73 34
    -153 37 -49 1 -103 -2 -120 -7z"/>
    <path d="M777 1020 c-26 -21 -27 -25 -27 -117 0 -78 4 -102 20 -128 21 -34 52
    -59 95 -75 l25 -10 0 149 c0 127 -3 152 -17 169 -27 32 -64 37 -96 12z"/>
    <path d="M3996 1764 c-91 -28 -186 -151 -186 -241 l0 -23 -155 0 c-166 0 -205
    -8 -254 -53 -47 -43 -61 -92 -61 -214 l0 -113 -32 0 c-74 -1 -178 -74 -220
    -154 -25 -49 -34 -137 -19 -191 27 -103 112 -183 217 -206 l54 -12 0 -199 c0
    -220 5 -247 63 -306 17 -18 47 -37 67 -42 21 -6 268 -10 623 -10 634 0 628 0
    686 53 53 49 61 85 61 303 l0 201 54 12 c130 29 226 144 226 272 0 64 -29 138
    -73 186 -47 51 -125 93 -174 93 l-33 0 0 113 c0 122 -14 171 -61 214 -49 45
    -88 53 -254 53 l-155 0 0 23 c0 93 -95 213 -190 241 -65 20 -120 19 -184 0z
    m654 -1014 l0 -560 -560 0 -560 0 0 560 0 560 560 0 560 0 0 -560z"/>
    <path d="M3755 1020 c-11 -4 -33 -22 -50 -40 -26 -27 -30 -38 -30 -90 0 -55 3
    -62 37 -96 67 -67 168 -54 218 28 66 109 -57 248 -175 198z"/>
    <path d="M4302 1011 c-94 -60 -94 -184 0 -241 58 -35 125 -22 178 35 21 22 25
    36 25 86 0 54 -3 61 -37 95 -46 47 -114 57 -166 25z"/>
    <path d="M3720 465 l0 -95 370 0 370 0 0 95 0 95 -370 0 -370 0 0 -95z"/>
    <path d="M2262 1048 c-20 -20 -15 -30 50 -95 l62 -63 -63 -64 c-44 -44 -62
    -69 -58 -80 15 -37 38 -29 103 35 l64 63 64 -63 c65 -64 88 -72 103 -35 4 11
    -14 36 -58 80 l-63 64 63 64 c64 65 76 97 37 104 -12 3 -40 -18 -82 -59 l-64
    -63 -63 62 c-65 65 -75 70 -95 50z"/>
    </g>
    </svg>`;

    public static readonly COPILOT_BLACK = `<svg width="917" height="318" viewBox="0 0 917 318" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M284 158.5C284 227.812 228.036 284 159 284C89.9644 284 34 227.812 34 158.5C34 89.1883 89.9644 33 159 33C228.036 33 284 89.1883 284 158.5Z" fill="black"/>
    <path d="M159.454 66C126.816 66 99.4735 90.4461 95.4565 122.52L95.3652 123.485V123.669V123.853C95.137 125.277 95.0456 126.702 95 128.172V218.375C95 236.204 109.196 250.724 126.862 251H127.455C145.167 251 159.591 236.709 159.865 218.926V214.101C134.485 211.758 114.994 190.528 114.583 164.887V145.634C114.902 127.805 129.51 113.56 147.221 113.835C164.521 114.111 178.489 128.172 178.809 145.634V192.32C205.193 184.049 224 159.373 224 130.608C223.954 94.9493 195.059 66 159.454 66Z" fill="white"/>
    <path d="M146.71 133H146.477C139.202 133 133.233 138.695 133 145.859V164.184C133 179.477 144.238 192.52 159.58 194.954L160 195V146.273C160 139.016 154.078 133.138 146.71 133Z" fill="white"/>
    <path d="M159.5 0C71.4083 0 0 71.1845 0 159C0 246.816 71.4083 318 159.5 318C247.592 318 319 246.816 319 159C319 71.1845 247.592 0 159.5 0ZM180.263 211.909L179.163 212.183L178.887 212.228V218.488C178.887 246.222 156.842 268.929 129.021 269.843H128.196H127.325C99.1833 269.843 76.2667 247.364 75.8083 219.356V218.488V129.302C75.8083 126.972 75.9458 124.687 76.2667 122.357L76.3125 121.946L76.45 120.895C81.5375 80.3681 115.775 49.3905 157.025 48.1569L158.263 48.1112H159.546C205.792 48.1112 243.283 85.3483 243.283 131.312C243.237 169.828 216.746 202.679 180.263 211.909Z" fill="white"/>
    <path d="M866.682 117.158V83.6842C866.682 65.2737 851.586 50.2105 833.136 50.2105H782.818C782.818 22.4274 760.343 0 732.5 0C704.657 0 682.182 22.4274 682.182 50.2105H631.864C613.414 50.2105 598.318 65.2737 598.318 83.6842V117.158C570.475 117.158 548 139.585 548 167.368C548 195.152 570.475 217.579 598.318 217.579V284.526C598.318 302.937 613.414 318 631.864 318H833.136C851.586 318 866.682 302.937 866.682 284.526V217.579C894.525 217.579 917 195.152 917 167.368C917 139.585 894.525 117.158 866.682 117.158ZM833.136 284.526H631.864V83.6842H833.136V284.526ZM682.182 184.105C668.26 184.105 657.023 172.892 657.023 159C657.023 145.108 668.26 133.895 682.182 133.895C696.103 133.895 707.341 145.108 707.341 159C707.341 172.892 696.103 184.105 682.182 184.105ZM807.977 159C807.977 172.892 796.74 184.105 782.818 184.105C768.897 184.105 757.659 172.892 757.659 159C757.659 145.108 768.897 133.895 782.818 133.895C796.74 133.895 807.977 145.108 807.977 159ZM665.409 217.579H799.591V251.053H665.409V217.579Z" fill="white"/>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M404.915 130.346C407.247 128.015 411.027 128.015 413.358 130.346L462.33 179.318C464.661 181.649 464.661 185.429 462.33 187.761C459.998 190.092 456.218 190.092 453.886 187.761L404.915 138.79C402.584 136.458 402.584 132.678 404.915 130.346Z" fill="white"/>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M462.331 130.346C464.663 132.678 464.663 136.458 462.331 138.79L413.36 187.761C411.028 190.092 407.248 190.092 404.917 187.761C402.585 185.429 402.585 181.649 404.917 179.317L453.888 130.346C456.219 128.015 460 128.015 462.331 130.346Z" fill="white"/>
    </svg>`;

    /*
        ----------------
        |   Views   |
        ----------------
        View types for different views
    */
    public static readonly PIECES_ONBOARDING_VIEW_TYPE = 'pieces-onboarding';
    public static readonly PIECES_EXPANDED_SNIPPET_VIEW_TYPE =
        'pieces-expanded-snippet';
    public static readonly PIECES_SNIPPET_LIST_VIEW_TYPE =
        'pieces-snippet-list';

    /*
        ----------------
        |   SETTINGS   |
        ----------------
        Front end text within the Pieces plugin settings tab
    */
    public static readonly SETTINGS_KEY = 'jupyter-pieces:storage';
    public static readonly CLOUD_SELECT = 'Cloud Capabilities';
    public static readonly CLOUD_SELECT_DESC =
        "Select if you'd like to utilize cloud only, local only, or a blend of both.";
    public static readonly PORT_PROMPT = 'Pieces server port:';
    public static readonly PORT_DESCRIPTION = "Pieces' default port is 1000.";
    public static readonly PORT_VALUE =
        process.platform == 'linux' ? '5323' : '1000';
    public static readonly SHOW_TUTORIAL = 'Show Plugin Usage Tutorials';
    public static readonly TUTORIAL_DESCRIPTION =
        'Display some useful information about using Pieces in Obsidian.';
    public static readonly LOGIN_TITLE = 'Login';
    public static readonly LOGIN_DESC =
        'Start generating shareable links for your code snippets';
    public static readonly LOGOUT_TITLE = 'Logout';
    public static readonly LOGOUT_DESC =
        'You will no longer have the ability to generate shareable links or share via GitHub Gist.';
    public static readonly TOGGLE_AUTOOPEN =
        'Auto-Open Pieces List on Snippet Save';
    public static readonly TOGGLE_AUTOOPEN_DESC =
        'Automatically open the Pieces snippet list view when saving a snippet.';

    /*
      ---------------------
      |   SAVE SNIPPETS   |
      ---------------------
      notification text for saving a piece
    */
    public static readonly NO_SAVE_SELECTION =
        'Make sure you select some text before you save a snippet';
    public static readonly SAVE_SUCCESS = 'Success saving to Pieces';
    public static readonly SAVE_FAIL = 'Failed Saving to Pieces';
    public static readonly SAVE_EXISTS = 'Snippet already exists in Pieces';
    public static readonly NO_ACTIVE_CELL = 'No active cell found';
    public static readonly NO_CODE_CELL = 'No active code cell found';

    /*
        ------------------------
        |   SIGNIN / SIGNOUT   |
        ------------------------
        notification text for Pieces login / logout
    */
    public static readonly SIGNIN_SUCCESS = 'Successfully signed in!';
    public static readonly SIGNIN_FAIL = 'Unable to sign in.';
    public static readonly SIGNOUT_SUCCESS = 'Successfully signed out.';
    public static readonly SIGNOUT_FAIL = 'Unable to sign out.';
    public static readonly CONNECTION_FAIL =
        'Failed to connect to Pieces OS. Please check that Pieces OS is installed and running.';

    /*
        ----------------------
        |   SNIPPET DELETE   |
        ----------------------
        notification text for snippet deletions
    */
    public static readonly SNIPPET_DELETE_SUCCESS =
        'Your Snippet Was Successfully Deleted!';
    public static readonly SNIPPET_IS_DELETED =
        'Snippet has already been deleted.';
    public static readonly SNIPPET_DELETE_FAILURE =
        'Failed to delete snippet. Please ensure that Pieces OS is up-to-date, installed and running. If the problem persists please reach out to support at support@pieces.app.';

    /*
        ---------------------------------
        |  CLOUD CONNECT / DISCONNECT   |
        ---------------------------------
        notification text for cloud handling
    */
    public static readonly LOGIN_TO_POS_CLOUD =
        'Please login to Pieces OS in order to connect to Pieces cloud.';
    public static readonly CLOUD_CONNECT_FAIL =
        'Unable to connect to Pieces cloud, please wait a minute an try again.';
    public static readonly CLOUD_CONNECT_SUCCESS =
        'Successfully connected to Pieces cloud.';
    public static readonly CLOUD_CONNECT_INPROG =
        'Pieces cloud is still connecting please try again later.';
    public static readonly CLOUD_DISCONNECT_ALR =
        'Already disconnected from Pieces cloud.';
    public static readonly CLOUD_DISCONNECT_SUCCESS =
        'Successfully disconnected from Pieces cloud.';
    public static readonly CLOUD_DISCONNECT_FAIL =
        'Failed to disconnect from Pieces cloud, please try again.';
    public static readonly CORE_PLATFORM_MSG =
        'Pieces for Developers ⎸ Core Platform runs offline and on-device to power our IDE and Browser extensions.';
    public static readonly LOGIN_TO_POS = 'Please login to Pieces OS';
    public static readonly LINK_GEN_SUCCESS = 'Shareable Link Generated!';
    public static readonly LINK_GEN_COPY = 'Sharable link copied to clipboard!';
    public static readonly LINK_GEN_FAIL =
        'Failed to generate link. Please ensure that Pieces OS is up-to-date, installed and running. If the problem persists please reach out to support at support@pieces.app.';

    /*
        -----------------------
        |   SEARCH SNIPPETS   |
        -----------------------
    */
    public static readonly SEARCH_SUCCESS = 'Snippet search success!';
    public static readonly SEARCH_FAILURE =
        'Something went wrong while searching for your snippets, if the issue persists please reach out to support at support@pieces.app.';

    /*
        -----------------------------------
        |   TEXT FOR POS DOWNLOAD MODAL   |
        -----------------------------------
        This is shown in the 'download-pos-modal'
        if we are not able to contact POS on their machine
    */
    public static readonly INSTALL_TEXT =
        'Please download, install, and run our core dependency to use Pieces with Obsidian:';
    public static readonly PIECES_ONDEVICE_COPY =
        'Pieces for Developers | Core Platform runs offline and on-device to power our IDE and Browser Extensions';

    /*
    -----------------------------------
    |   TEXT FOR ExpandView Problem   |
    -----------------------------------
    This is shown in the 'general text view'
    if we are not able to expand their snippet
    */
    public static readonly EXPAND_ERROR =
        'Error expanding snippet, check the `Snippet ID` and try again.';

    /*
        ------------------------------
        |   TEXT FOR WELCOME MODAL   |
        ------------------------------
        This is shown within 'onboarding-modal'
        if it is the first time the user is loading the extension
    */

    public static readonly WELCOME_TEXT = 'Welcome to Pieces for Developers!';
    public static readonly SAVE_INSERT_SEARCH =
        'Save, insert, and search your snippets.';

    // Saving snippets
    public static readonly SAVE_SNIPPET = 'Save a snippet';
    public static readonly SAVE_EXPLANATION =
        'Select the snippet you would like to save to Pieces, right click, and click the "Save to Pieces" button';
    public static readonly SAVE_SHORTCUT_EX =
        'Or you can use the keyboard shortcut: MOD + SHIFT + P';

    // Viewing Snippets
    public static readonly VIEW_SNIPPETS = 'Viewing your Snippets';
    public static readonly VIEW_SNIPPET_EXPLANATION =
        'In order to view your saved snippets, just click on the "Pieces" icon on your ribbon bar.';

    // Inserting Snippets
    public static readonly INSERT_SNIPPET = 'Insert a snippet';
    public static readonly INSERT_SNIPPET_EXPLANATION =
        'In order to insert a snippet, navigate to the snippet on the Pieces view, click the "copy snippet" button, and paste it into your editor';

    // Searching Snippets
    public static readonly SEARCH_SNIPPET = 'Search for a Snippet';
    public static readonly SEARCH_SNIPPET_EXPLANATION =
        'To search for a snippet, navigate to the Pieces view, and type your query into the search box. Once you are done, click the "X" and it will clear your search.';
    public static readonly UPDATE_OS =
        'In order to use the Pieces for Developers Obsidian Plugin, you must have Pieces OS version 5.1.2 or greater! Please update your Pieces OS';

    /*
		|------------------|
		|	UPDATE ASSET   |
		|------------------|
	*/
    public static readonly RECLASSIFY_SUCCESS =
        'Snippet Successfully Reclassified';
    public static readonly RECLASSIFY_FAILURE =
        'Error Reclassifying snippet, please try again.';
    public static readonly UPDATE_SUCCESS = 'Snippet successfully updated';
    public static readonly UPDATE_FAILURE =
        'Error updating snippet, please try again.';

    /*
		|------------------|
		|	COPY TO CLIP   |
		|------------------|
	*/

    public static readonly COPY_SUCCESS = 'Snippet copied to clipboard';

    /*
        |--------------------|
        | SNIPPET DISCOVERY  |
        |--------------------|
    */

    public static readonly DISCOVERY_SUCCESS = 'Snippet Discovery Complete!';
    public static readonly DISCOVERY_FAILURE =
        'Something went wrong with Snippet Discovery, are you sure POS is installed, running, and up to date?';
}
