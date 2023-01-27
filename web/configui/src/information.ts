export type Information = {
  module: ModuleInf[];
  IO: string[];
  Recorder: string[];
  Field: string[];
};

export type ModuleInf = {
  name: string;
  input: {
    [key: string]: {
      required: boolean;
    };
  };
  output: {
    [key: string]: {};
  };
};
