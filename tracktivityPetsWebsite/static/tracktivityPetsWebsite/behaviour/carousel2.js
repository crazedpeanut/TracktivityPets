$(function() {
	$('#imagecaro').carouFredSel({
		width:'100%',
		items: 3,
//		items: {
//			visible: 1,
//			start:1
//		},
		auto: false,
		scroll: {
			items: 1,
			duration: 1000,
			timeoutDuration: 3000
		},
		prev: '#prev',
		next: '#next',
//		pagination: {
//			container:'#pager',
//			deviation: 1
//		}
	});
});
