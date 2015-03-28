$('.skillset').keydown(function(e){
if(e.keyCode==9) e.preventDefault();
});
$(function() {
function split( val ) {
return val.split( /,\s*/ );
}
function extractLast( term ) {
return split( term ).pop();
}
$( ".skillset" )
.keydown(function(e){
if(e.keyCode==9 || e.keyCode==13) e.preventDefault();
})
.autocomplete({
source: function( request, response ) {
$.getJSON( "/skills/get_skills/", {
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