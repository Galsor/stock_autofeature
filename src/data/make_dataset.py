# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import src.config as cfg
from src.data.stock import Stock

@click.command()
@click.argument('symbol', type=click.STRING)
def main(symbol:str):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f'Creating dataset for {symbol}')
    stock = Stock(symbol, save=True)



if __name__ == '__main__':
    logging.basicConfig(**cfg.LOGGING_CONFIG)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
