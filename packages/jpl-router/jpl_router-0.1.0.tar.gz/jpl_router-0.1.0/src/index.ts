import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the jpl_router extension.
 */

export const FetchData = (data: JSON) => {
  console.log(data);
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jpl_router:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jpl_router is activated!');

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jpl_router server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
