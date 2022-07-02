/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Value = {
    readonly id?: number;
    rate: {
        readonly id?: number;
        /**
         * Название
         */
        name: string;
        /**
         * Номинал
         */
        nominal?: number;
        code: string;
    };
    num_code: number;
    char_code: string;
    date: string;
    value: string;
};

