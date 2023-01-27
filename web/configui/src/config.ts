export type Config = {
  version: 1;
  basic: Basic_Config;
  instance: Instance_Declare[];
  link: Link_Declare[];
};

export type Basic_Config = {
  timestep: number;
  timeUnit: "hour" | "minute" | "second";
  timeEpoch: number;
  outputPath: string;
};

export type Instance_Declare = {
  name: string;
  field: string;
  init: Init_Declare;
};

export enum Init_Use {
  define = "define",
  no = "no",
}
export type Init_Declare = {
  [U in Init_Use]: {
    use: U;
    define?: U extends Init_Use.define ? Define_Declare : void;
  };
}[Init_Use];

export type Define_Declare = {
  method: string;
  config: object;
  data: object | null;
};

export type Link_Declare = {
  module: string;
  time: string;
  input: Input_Declare[];
  output: Output_Declare[];
  recordInside: Record_Declare[];
  record: Record_Declare[];
};

export enum Input_Use {
  instance = "instance",
  new = "new",
}
export type Input_Declare = {
  [U in Input_Use]: {
    into: string;
    use: U;
    instance?: U extends Input_Use.instance
      ? string
      : U extends Input_Use.new
      ? {
          field: string;
          init: Init_Declare;
        }
      : never;
  };
}[Input_Use];

export type Output_Declare = {
  catch: string;
  put: string;
};

export type Record_Declare = {
  catch: string;
  method: string;
  config: object;
  time: string;
};
