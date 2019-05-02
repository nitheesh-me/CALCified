chrome.browserAction.onClicked.addListener(function (tab) {
	chrome.tabs.create({
		index: 1,
		url: 'https://google.co.in/search?q=calculator'
	});
});

chrome.runtime.onInstalled.addListener(function (d){
	if (d.reason === "install") chrome.tabs.create(
		{
			url: 'https://google.co.in/search?q=calculator'
		},function () {})
})
