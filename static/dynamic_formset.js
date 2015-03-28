$(document).ready(function() {
// Code adapted from http://djangosnippets.org/snippets/1389/

	function updateElementIndex(el, prefix, ndx) {
		var id_regex = new RegExp('(' + prefix + '-\\d+-)');
		var replacement = prefix + '-' + ndx + '-';
		if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
		replacement));
		if (el.id) el.id = el.id.replace(id_regex, replacement);
		if (el.name) el.name = el.name.replace(id_regex, replacement);
	}

	function deleteForm(btn, prefix) {
		var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

		if (formCount > 1) {
			// Delete the item/form
			$(btn).parents('.item').remove();

			var forms = $('.item'); // Get all the forms

			// Update the total number of forms (1 less than before)
			$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

			var i = 0;
			// Go through the forms and set their indices, names and IDs
			for (formCount = forms.length; i < formCount; i++) {
				$(forms.get(i)).children().children().each(function() {
				  updateElementIndex(this, prefix, i);
				});
			}

		} // End if
	
		else {
			alert("You have to enter at least one open position item!");
		}
			return false;
	}


	function addForm(btn, prefix) {
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

	// You can only submit a maximum of 10 items
	if (formCount < 10) {
	// Clone a form (without event handlers) from the first form
	var row = $(".item:first").clone(false).get(0);
	
	$(row).find(".suggestions").html("");
		
	// Insert it after the last form
	$(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

	// Remove the bits we don't want in the new row/form
	// e.g. error messages
	$(".errorlist", row).remove();
	$(row).children().removeClass('error');

	// Relabel/rename all the relevant bits
	$(row).children().children().each(function() {
	updateElementIndex(this, prefix, formCount);
	if ( $(this).attr('type') == 'text' )
	  $(this).val('');
	});

	// Add an event handler for the delete item/form link
	$(row).find('.delete').click(function() {
	return deleteForm(this, prefix);
	});

	$(row).find('.skills').keydown(function() {
	return autocomplete(".skills", "/skills/get_skills");
	});

	$(row).find('.invited').keydown(function() {
	return autocompleteSmall(".invited", "/user/get_user/");
	});

	// Update the total form count
	$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);

	} // End if
	else {
	alert("Sorry, you can only enter a maximum of ten items.");
	}
	return false;
	}

	// Register the click event handlers
	$("#add").click(function() {
	return addForm(this, 'form');
	});

	$(".delete").click(function() {
	return deleteForm(this, 'form');
	});

	$(".skills").keydown(function() {
	return autocomplete(".skills", "/skills/get_skills/");
	});

	$(".invited").keydown(function() {
	return autocompleteSmall(".invited", "/user/get_user/");
	});

function autocompleteSmall(element, source) {
  $(element).autocomplete({
    source: source,
    minLength: 2,
    select: function( event, ui ) { 
            alert('You selected ' + ui.item.label + '. Username: ' + ui.item.value);
        }
  })
}


function autocomplete(element, source) {
	$(element).keydown(function(e){
	if(e.keyCode==9 || e.keyCode==13) e.preventDefault();
	});
	
	$(function() {
	function split( val ) {
	return val.split( /,\s*/ );
	}
	function extractLast( term ) {
	return split( term ).pop();
	}
	$(element).keydown(function(e){
	if(e.keyCode==9 || e.keyCode==13) e.preventDefault();
	})
	.autocomplete({
	source: function( request, response ) {
	$.getJSON( source, {
	term: extractLast( request.term )
	}, response );
	},
	search: function() {
	// custom minLength
	var term = extractLast( this.value );
	if ( term.length < 2 ) {
	return false;
	}
	},
	focus: function() {
	// prevent value inserted on focus
	return false;
	},
	select: function( event, ui ) {
	var terms = split( this.value );
	// remove the current input
	terms.pop();
	// add the selected item
	terms.push( ui.item.value );
	// add placeholder to get the comma-and-space at the end
	terms.push( "" );
	this.value = terms.join( ", " );
	return false;
	}
	});
	});
	}
});