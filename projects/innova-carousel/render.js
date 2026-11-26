// Screenshot every .slide in slides.html at 2x into out/raw/sN.png.
const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
	const dir = __dirname;
	fs.mkdirSync(path.join(dir, 'out', 'raw'), {recursive: true});
	const browser = await chromium.launch();
	const page = await browser.newPage({viewport: {width: 1080, height: 1350}, deviceScaleFactor: 2});
	await page.goto('file://' + path.join(dir, 'slides.html'));
	await page.evaluate(() => document.fonts.ready);
	const slides = await page.$$('.slide');
	for (let i = 0; i < slides.length; i++) {
		await slides[i].screenshot({path: path.join(dir, 'out', 'raw', `s${i + 1}.png`)});
	}
	await browser.close();
	console.log(slides.length, 'slides rendered');
})();
