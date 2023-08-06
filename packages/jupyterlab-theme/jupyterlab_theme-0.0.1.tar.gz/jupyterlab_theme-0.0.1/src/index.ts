import { ILabShell, JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { LabIcon, jupyterFaviconIcon, jupyterIcon, jupyterlabWordmarkIcon } from '@jupyterlab/ui-components';
import { Widget } from '@lumino/widgets';

/**
 * A NayaOne theme and logo replacement for JupyterLab
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: '@nayaone/jupyterlab-theme:plugin',
    requires: [IThemeManager, ILabShell],
    activate: (app: JupyterFrontEnd, manager: IThemeManager, shell: ILabShell) => {
        const style = '@nayaone/jupyterlab-theme/index.css';

        // Create the nayaone logo
        const nayaone_svg = '<svg width="372" height="402" viewBox="0 0 372 402" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0.000244141 0.692413H121.616V401.308H0.000244141V0.692413Z" fill="#1F2D4C"/><path fill-rule="evenodd" clip-rule="evenodd" d="M372 0.692413H250.384V1.83815H246.807L121.615 123.453H250.384V401.308H372V123.453V1.83815V0.692413Z" fill="#583BC6"/></svg>';
        const nayaone_icon = new LabIcon({ name: 'ui-components:nayaone', svgstr: nayaone_svg });

        // Attach the nayaone logo in the top left
        const logo = new Widget();
        nayaone_icon.element({
            container: logo.node,
            elementPosition: 'center',
            margin: '2px 2px 2px 8px',
            height: 'auto',
            width: '16px'
        });
        logo.id = 'jp-nayaoneLogo';
        shell.add(logo, 'top', { rank: 0 });

        // Set the icons elsewhere
        jupyterFaviconIcon.svgstr = nayaone_svg;
        jupyterIcon.svgstr = nayaone_svg;
        jupyterlabWordmarkIcon.svgstr = nayaone_svg;

        // Register the plugin
        manager.register({
            name: 'nayaone',
            isLight: true,
            themeScrollbars: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};

export default plugin;
