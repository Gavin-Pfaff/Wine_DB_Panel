const { app, BrowserWindow } = require('electron');

app.whenReady().then(() => {
	const win = new BrowserWindow({ width: 1200, height: 800 });
	win.loadFile('Frontend/index.html');
});