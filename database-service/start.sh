#!/bin/sh

export $(cat .env)

flask run --host 0.0.0.0

