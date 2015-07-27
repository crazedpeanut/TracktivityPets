
	$('#carousel').carouFredSel({
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
		prev: '#prev2',
		next: '#next2',
		synchronise: ['#imagecaro', true, true]
//		pagination: {
//			container:'#pager',
//			deviation: 1
//		}
	});

$('#next2').click(function(){
	$("#carousel, #imagecaro").trigger("next");
});

$('#prev2').click(function(){
	$("#carousel, #imagecaro").trigger("prev");
});

$('#imagecaro').carouFredSel({
	auto : false
});
