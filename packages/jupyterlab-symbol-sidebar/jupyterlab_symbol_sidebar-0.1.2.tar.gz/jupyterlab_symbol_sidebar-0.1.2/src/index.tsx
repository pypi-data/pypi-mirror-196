import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILabShell
} from '@jupyterlab/application';

import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import {codeList} from './code';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_symbol_sidebar:plugin',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('JupyterLab extension jupyterlab_symbol_sidebar is activated!');

    var checkboxCopy = false;

    function SymbolsSidebar() {
      var list = codeList;
      return (
        <div className="sidebar-container">
          <div className="notice">Click on the icon will insert it to the cell</div>
          <label className="checkbox">
            <input
              type="checkbox"
              onChange={() => {
                  checkboxCopy = !checkboxCopy;
                }}
            />
            Copy to clipboard
          </label>
              <div className="block_container">
                {list.map((item,i) => 
                  <div 
                    className="block_container_element"
                    key={i} 
                    onClick={() => iconClick(item.unicode)}
                  >
                    {item.unicode}
                    <div>{item.name}</div>
                  </div>)}
              </div>
        </div>
        );
    }

    function iconClick(code:any) {
      if (checkboxCopy)
        navigator.clipboard.writeText(JSON.parse(`["`+code+`"]`)[0].toString())
      else
        app.commands.execute('unicode:insert', { text: JSON.parse(`["`+code+`"]`)[0].toString() });                 
    }

    const newWidget = () => {
      // Create a blank content widget inside of a MainAreaWidget
      const widget = ReactWidget.create(
        <SymbolsSidebar />
      );
      widget.id = 'jupyterlab_symbol_sidebar';
      widget.title.label = 'Symbols';
      widget.title.closable = true;
      return widget;
    }
    let widget = newWidget();

    // let summary = document.createElement('p');
    // widget.node.appendChild(summary);
    // summary.innerText = "Hello, World!";

    shell.add(widget, 'left');
  }
};

export default extension;
