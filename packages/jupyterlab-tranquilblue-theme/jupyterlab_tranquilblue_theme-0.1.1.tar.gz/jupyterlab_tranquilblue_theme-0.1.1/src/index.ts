import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_tranquilblue_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_tranquilblue_theme:plugin',
  description: 'A JupyterLab theme in cool blue and purple extension.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab_tranquilblue_theme is activated!');
    const style = 'jupyterlab_tranquilblue_theme/index.css';

    manager.register({
      name: 'jupyterlab_tranquilblue_theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
