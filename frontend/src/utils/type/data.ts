import { IAlreadyPacked, IGoods, IRecPacking, IUser } from "./main";

export interface IRegisterTable {
  userId: number;
  inputValue: string;
}

export interface IResponseTable {
  success: boolean;
  token: string;
}

export interface IRegisterPrinter {
  inputValue: string;
}

export interface IResponsePrinter {
  success: boolean;
  user: IUser;
}

export interface IDataValues<T> {
  success?: boolean;
  status?: '';
  data: T;
}

export interface IOrder {
  partition: string;
  orderkey: string;
  goods: Array<IGoods>
  recomend_packing: Array<Array<IRecPacking>>
  already_packed: Array<Array<IAlreadyPacked>>;
}

export interface IBarcode {
  barcode: string;
  imei?: string;
  honest_sign?: string;
}

export interface IStatus {
  status: string;
}