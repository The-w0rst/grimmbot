# Setup Guide

This repository expects your API credentials in a local `.env` file. An example file is provided as `.env.example`.

1. Copy `.env.example` to `.env`:
   
   ```sh
   cp .env.example .env
   ```

2. Open `.env` in a text editor and fill in your personal API keys and tokens.

The application code should load these variables from `.env` so you never commit your secrets to version control.

