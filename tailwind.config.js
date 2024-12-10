
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './node_modules/svelte-ux/**/*.{svelte,ts}',
    './node_modules/layerchart/**/*.{svelte,ts}'
  ],
  theme: {
    extend: {
      colors:{
        // LayerChart tokens mapped to shadcn-svelte colors.
				surface: {
					content: "hsl(var(--card-foreground) / <alpha-value>)",
					100: "hsl(var(--background) / <alpha-value>)",
					200: "hsl(var(---muted) / <alpha-value>)",
					// not sure what color maps here (should be darker than 200).  Could add a new color to `app.css`
					300: "hsl(var(--background) / <alpha-value>)"
				},
      }
  },
  plugins: [],
}
}
