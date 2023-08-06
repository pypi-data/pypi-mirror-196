import {
  ICommandPalette
} from '@jupyterlab/apputils';

import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  IMainMenu
} from '@jupyterlab/mainmenu';

import '../style/index.css';

namespace CommandIDs {
  export const help = 'nayaone:help';
}
/**
 * Initialization data for the upload_disable extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'disable_upload',
  autoStart: true,
  requires: [
    ICommandPalette,
    IMainMenu
  ],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, mainMenu: IMainMenu) => {
    app.commands.addCommand(CommandIDs.help, {
      label: 'Support Page',
      execute: () => {
        window.open('https://google.com','_blank');
      }
    });
    mainMenu.helpMenu.addGroup([{ command: CommandIDs.help }], 20);
  }
};

export default extension;