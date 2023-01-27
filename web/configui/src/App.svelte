<script lang="ts">
  import type { Information } from "./information";
  import { Input_Use, Init_Use, type Instance_Declare } from "./config";
  import jsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
  import * as monaco from "monaco-editor";
  import { onMount } from "svelte";
  import type { Config, Link_Declare } from "./config";
  import * as information from "./information.json";

  const inf: Information = information;
  const ModulesList = inf.module;
  const IO = inf.IO;
  const Recorder = inf.Recorder;
  const Field = inf.Field;

  function getModule(name: string) {
    for (const i in ModulesList) {
      if (ModulesList[i].name === name) {
        return ModulesList[i];
      }
    }
  }

  self.MonacoEnvironment = {
    getWorker(_: string, label: string) {
      return new jsonWorker();
    },
  };

  let config: Config = {
    version: 1,
    basic: {
      timestep: 1,
      timeUnit: "hour",
      timeEpoch: 3,
      outputPath: "output/web",
    },
    instance: [],
    link: [],
  };

  const initStr = JSON.stringify(config, null, "  ");
  let editBox = {
    edit: initStr,
    target: "config",
    name: "",
    update: () => {
      config = JSON.parse(editBox.edit);
    },
  };

  $: if (editBox.target === "config") {
    editBox.edit = JSON.stringify(config, null, "  ");
  }

  $: if (editor) {
    editor.setValue(editBox.edit);
    format();
  }

  function editConfig() {
    editBox.target = "config";
    editBox.name = "";
    editBox.edit = JSON.stringify(config, null, "  ");
    editBox.update = () => {
      config = JSON.parse(editBox.edit);
    };
  }

  function editIns(name: string) {
    editBox.target = "init";
    editBox.name = name;

    editBox.edit = JSON.stringify(
      config.instance.filter((item) => {
        return item.name === name;
      })[0].init,
      null,
      "  "
    );

    editBox.update = () => {
      config.instance.filter((item) => {
        return item.name === name;
      })[0].init = JSON.parse(editBox.edit);
    };
  }

  $: if (editBox.target === "init") {
    editBox.edit = JSON.stringify(
      config.instance.filter((item) => {
        return item.name === editBox.name;
      })[0].init,
      null,
      "  "
    );
  }

  let editor: monaco.editor.IStandaloneCodeEditor;

  onMount(() => {
    editor = monaco.editor.create(
      document.getElementById("editor") as HTMLElement,
      {
        value: "", // 编辑器初始显示文字
        language: "json",
        automaticLayout: true, // 自适应布局
        theme: "vs-dark",
        foldingStrategy: "indentation",
        renderLineHighlight: "all",
        selectOnLineNumbers: true,
        minimap: {
          enabled: false,
        },
        readOnly: false,
        fontSize: 16, // 字体大小
        scrollBeyondLastLine: false, // 取消代码后面一大段空白
        overviewRulerBorder: false, // 不要滚动条的边框
        tabSize: 2,
        insertSpaces: true,
      }
    );
  });

  function format() {
    editor.getAction("editor.action.formatDocument").run(); //自动格式化代码
  }

  function save() {
    editBox.edit = editor.getValue();
    editBox.update();
    config = config;
  }

  let selectModule: string;
  function addLink() {
    const mo = selectModule;
    console.log(selectModule);
    const newMo: Link_Declare = {
      module: mo,
      time: "always",
      input: [],
      output: [],
      recordInside: [],
      record: [],
    };
    config.link.push(newMo);
    config = config;
  }

  let selectField: string;
  let newFieldName: string;
  let newInitWay: Init_Use;
  let newDefineMethod: string;
  let initUse = Object.keys(Init_Use);
  //initUse = initUse.slice(initUse.length / 2);
  function addIns() {
    const newIns: Instance_Declare = {
      name: newFieldName,
      field: selectField,
      init: {
        use: Init_Use.no,
      },
    };
    if (newInitWay === "define") {
      newIns.init = {
        use: Init_Use.define,
        define: {
          method: newDefineMethod,
          config: {},
          data: null,
        },
      };
    }
    config.instance.push(newIns);
    config = config;
  }

  let selectLinkId = -1;
  let selectInName = "";
  let selectUse: Input_Use;
  let in2Ins = "";
  $: if (selectLinkId !== -1 && selectInName !== "") {
    const input = config.link[selectLinkId].input.filter(
      (input) => input.into === selectInName
    )[0];
    selectUse = input.use;
    if (input.use === Input_Use.instance) {
      in2Ins = input.instance;
    }
  }
</script>

<main>
  <div id="left">
    {JSON.stringify(config, null, "  ")}
    {#each config.link as link, linkid}
      <div class="link">
        {link.module}
        <br />
        time <input bind:value={link.time} />
        <div>
          In
          {#each Object.keys(getModule(link.module).input) as inName}
            <div>
              {inName}
            </div>
          {/each}
        </div>
        <div>Out</div>
        <div>RecordInside</div>
      </div>
    {/each}
    <div>
      <select bind:value={selectModule}>
        {#each ModulesList as mo}
          <option value={mo.name}>
            {mo.name}
          </option>
        {/each}
      </select>
      <button on:click={addLink}>Add Module</button>
    </div>
  </div>
  <div id="middle">
    {#each config.instance as instance}
      <div>{instance.name}</div>
      <button
        on:click={() => {
          editIns(instance.name);
        }}>edit</button
      >
    {/each}
    <select bind:value={selectField}>
      {#each Field as field}
        <option value={field}>
          {field}
        </option>
      {/each}
    </select>
    Name <input bind:value={newFieldName} />
    <select bind:value={newInitWay}>
      {#each initUse as inituse}
        <option value={inituse}>
          {inituse}
        </option>
      {/each}
    </select>
    {#if newInitWay === "define"}
      IO
      <select bind:value={newDefineMethod}>
        {#each IO as method}
          <option value={method}>
            {method}
          </option>
        {/each}
      </select>
    {/if}
    <button on:click={addIns}>Add Instance</button>
  </div>
  <div id="right">
    <div>
      <button on:click={editConfig}>config</button>
      <button on:click={format}>format</button><button on:click={save}
        >save</button
      >
    </div>
    <div id="editor" />
  </div>
</main>

<style>
  main {
    width: 100vw;
    display: flex;
  }
  #left {
    height: 100vh;
    width: 30vw;
  }
  #middle {
    height: 100vh;
    width: 30vw;
  }
  #right {
    height: 100vh;
    width: 40vw;
    display: flex;
    flex-direction: column;
  }
  #editor {
    flex-grow: 1;
    height: max-content;
  }
</style>
