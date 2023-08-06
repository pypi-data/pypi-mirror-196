#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.0.1"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"

from concurrent.futures.thread import ThreadPoolExecutor
from pywifi import const


class StopTransmission(Error):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from .raw import raw
from .filters import filters
from handlers import handlers
from .emoji import emoji
from enums import enums
from .client import Client
from .sync import idle, compose

# import {* as} types from './types';
# import {* as} filters from './filters';
# import {* as} handlers from './handlers';
# import {* as} emoji from './emoji';
# import {* as} enums from './enums';
# import { Client } from './client';
# import { idle, compose } from './sync';

const
crypto_executor: ThreadPoolExecutor = ThreadPoolExecutor(1, "CryptoWorker")
