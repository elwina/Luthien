<script lang="ts">
  import jsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
  import * as monaco from "monaco-editor";
  import { onMount } from "svelte";

  self.MonacoEnvironment = {
    getWorker(_: string, label: string) {
      return new jsonWorker();
    },
  };

  onMount(() => {
    let editor: monaco.editor.IStandaloneCodeEditor;

    editor = monaco.editor.create(
      document.getElementById("codeEditBox") as HTMLElement,
      {
        value: "asd", // 编辑器初始显示文字
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
</script>

<main>
  <div id="codeEditBox" style:height="100vh" style:width="50vw" />
</main>
