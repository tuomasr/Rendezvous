$(function() {
	$("#id_country").keydown(function() {
	return autocompleteSmall("#id_country", "/geo/country/");
	});

	$("#id_city").keydown(function() {
	return autocompleteSmall("#id_city", "/geo/city/");
	});
	
	$(".location").keydown(function() {
	return autocompleteSmall(".location", "/geo/location/");
	});


	function autocompleteSmall(element, source) {
	  $(element).autocomplete({
		source: source,
		minLength: 2,
	  });
	}
});