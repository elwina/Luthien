<script lang="ts">
  import jsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
  import * as monaco from "monaco-editor";
  import { onMount } from "svelte";
  import type { Config, Link_Declare } from "./config";
  import { module as modules, IO, Recorder } from "./information.json";

  function getModuleIn(name: string) {
    for (const i in modules) {
      if (modules[i].name === name) {
        return modules[i];
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

  let editBox = {
    edit: JSON.stringify(config),
    target: "config",
    update: () => {
      config = JSON.parse(editBox.edit);
    },
  };

  $: if (editBox.target === "config") {
    editBox.edit = JSON.stringify(config);
  }

  $: if (editor) {
    editor.setValue(editBox.edit);
    format();
  }

  let editor: monaco.editor.IStandaloneCodeEditor;

  onMount(() => {
    editor = monaco.editor.create(
      document.getElementById("editor") as HTMLElement,
      {
        value: JSON.stringify(config), // 编辑器初始显示文字
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
      }
    );
  });

  function format() {
    editor.getAction("editor.action.formatDocument").run(); //自动格式化代码
  }

  function save() {
    editBox.edit = editor.getValue();
    editBox.update();
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
</script>

<main>
  <div id="left">
    {JSON.stringify(config)}
    {#each config.link as link}
      <div class="link">
        {link.module}
        <div>
          In
          {#each Object.keys(getModuleIn(link.module).input) as inName}
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
        {#each modules as mo}
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
    {/each}
  </div>
  <div id="right">
    <div>
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
