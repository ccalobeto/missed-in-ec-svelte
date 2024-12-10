# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Setup Python
Choose your python virtual environment in your VS Code placed in the botton. In my case `3.12.3('py312':conda)`

## Download CSV files
Go to [Ecuador datos abiertos](https://www.datosabiertos.gob.ec/dataset/personas-desaparecidas), download the excel files and convert them to csv files. Be careful with ',' for decimals in google sheets. Move the converted files to `static/data/input`.

## Executing scripts 
Run these scripts

To install your python libraries
```javascript
npm run python:dependencies
```

To load a csv file, clean and generate one cumulated csv file
```javascript
npm run data:generate
```

To generate a json file with all summaries for your svelte project
```javascript
npm run data:summary
```

## setup layerchart
### setup svelte ux
```bash
npm install svelte-ux
```
### setup tailwind
use this [tutorial](https://tailwindcss.com/docs/guides/sveltekit) to install tailwind with sveltekit
