/* New: Variable searchhi_string to keep track of words being searched. */
var searchhi_string = '';

/* New from Rob Nitti, who credits 
 * http://bytes.com/groups/javascript/145532-replace-french-characters-form-inp
 * The code finds accented vowels and replaces them with their unaccented version. */
function stripVowelAccent(str)
{
	var rExps=[ /[\xC0-\xC2]/g, /[\xE0-\xE2]/g,
		/[\xC8-\xCA]/g, /[\xE8-\xEB]/g,
		/[\xCC-\xCE]/g, /[\xEC-\xEE]/g,
		/[\xD2-\xD4]/g, /[\xF2-\xF4]/g,
		/[\xD9-\xDB]/g, /[\xF9-\xFB]/g ];

	var repChar=['A','a','E','e','I','i','O','o','U','u'];

	for(var i=0; i<rExps.length; ++i)
		str=str.replace(rExps[i],repChar[i]);

	return str;
}

/* http://www.kryogenix.org/code/browser/searchhi/ */
/* Modified 20021006 to fix query string parsing and add case insensitivity */
/* Modified 20111112 to count matches */
function highlightWord(node,word,doc) {
     doc = typeof(doc) != 'undefined' ? doc : document;
     count_matches = 0;
	// Iterate into this nodes childNodes
	if (node.hasChildNodes) {
		var hi_cn;
		for (hi_cn=0;hi_cn<node.childNodes.length;hi_cn++) {
			count_matches = count_matches + highlightWord(node.childNodes[hi_cn],word,doc);
		}
	}

	// And do this node itself
	if (node.nodeType == 3) { // text node
		tempNodeVal = stripVowelAccent(node.nodeValue.toLowerCase());
		tempWordVal = stripVowelAccent(word.toLowerCase());
		if (tempNodeVal.indexOf(tempWordVal) != -1) {
			pn = node.parentNode;
			if (pn.className != "searchword") {
                    count_matches = count_matches + 1;
				// word has not already been highlighted!
				nv = node.nodeValue;
				ni = tempNodeVal.indexOf(tempWordVal);
				// Create a load of replacement nodes
				before = doc.createTextNode(nv.substr(0,ni));
				docWordVal = nv.substr(ni,word.length);
				after = doc.createTextNode(nv.substr(ni+word.length));
				hiwordtext = doc.createTextNode(docWordVal);
				hiword = doc.createElement("span");
				hiword.className = "searchword";
				hiword.appendChild(hiwordtext);
				pn.insertBefore(before,node);
				pn.insertBefore(hiword,node);
				pn.insertBefore(after,node);
				pn.removeChild(node);
			}
		}
	}

     return count_matches;
}

function unhighlightWord(node,word,doc) {
     doc = typeof(doc) != 'undefined' ? doc : document;
	// Iterate into this nodes childNodes
	if (node.hasChildNodes) {
		var hi_cn;
		for (hi_cn=0;hi_cn<node.childNodes.length;hi_cn++) {
			unhighlightWord(node.childNodes[hi_cn],word,doc);
		}
	}

	// And do this node itself
	if (node.nodeType == 3) { // text node
		tempNodeVal = node.nodeValue.toLowerCase();
		tempWordVal = word.toLowerCase();
		if (tempNodeVal.indexOf(tempWordVal) != -1) {
			pn = node.parentNode;
			if (pn.className == "searchword") {
				prevSib = pn.previousSibling;
				nextSib = pn.nextSibling;
				nextSib.nodeValue = prevSib.nodeValue + node.nodeValue + nextSib.nodeValue;
				prevSib.nodeValue = '';
				node.nodeValue = '';
			}
		}
	}
}

function unhighlight(node) {
	// Iterate into this nodes childNodes
	if (node.hasChildNodes) {
		var hi_cn;
		for (hi_cn=0;hi_cn<node.childNodes.length;hi_cn++) {
			unhighlight(node.childNodes[hi_cn]);
		}
	}

	// And do this node itself
	if (node.nodeType == 3) { // text node
		pn = node.parentNode;
		if( pn.className == "searchword" ) {
			prevSib = pn.previousSibling;
			nextSib = pn.nextSibling;
			nextSib.nodeValue = prevSib.nodeValue + node.nodeValue + nextSib.nodeValue;
			prevSib.nodeValue = '';
			node.nodeValue = '';
		}
	}
}

function googleSearchHighlight(doc) {
     doc = typeof(doc) != 'undefined' ? doc : document;
	if (!doc.createElement) return 0;
	ref = doc.referrer;
        ref = ref.replace(/\/search\/web\//,'?search&q='); // Most WebCrawler searches
	if (ref.indexOf('?') == -1) return 0;
     count_matches = 0;
	qs = ref.substr(ref.indexOf('?')+1);
        qsa = qs.split('#');
        qs = qsa[0];
        qs = qs.replace(/(^|&)p=Q&ts=e&/,'&'); // Most Eurekster searches
        qs = qs.replace(/(^|&)query=/,'&q='); // Most Lycos searches
        qs = qs.replace(/(^|&)key=/,'&q='); // Most Walhello searches
        qs = qs.replace(/(^|&)keywords=/i,'&q='); // Most Overture searches
        qs = qs.replace(/(^|&)searchfor=/,'&q='); // Most Mysearch.com searches
        qs = qs.replace(/(^|&)qt=/,'&q='); // Most Acoona.com searches
        qs = qs.replace(/(^|&)s=/,'&q='); // Most Technirati GET searches
	qsa = qs.split('&');
	for (i=0;i<qsa.length;i++) {
		qsip = qsa[i].split('=');
	        if (qsip.length == 1) continue;
        	if (qsip[0] == 'q' || qsip[0] == 'p' || qsip[0] == 'w') { // q= for Google, p= for Yahoo, w= for Eurekster
			// Trim leading and trailing spaces after unescaping
			qsip[1] = unescape(qsip[1]).replace(/^\s+|\s+$/g, "");
			if( qsip[1] == '' ) continue;
                        phrases = qsip[1].replace(/\+/g,' ').split(/\"/);
			for(p=0;p<phrases.length;p++) {
			        phrases[p] = unescape(phrases[p]).replace(/^\s+|\s+$/g, "");
				if( phrases[p] == '' ) continue;
				if( p % 2 == 0 ) words = phrases[p].replace(/([+,()]|%(29|28)|\W+(AND|OR)\W+)/g,' ').split(/\s+/);
				else { words=Array(1); words[0] = phrases[p]; }
	                	for (w=0;w<words.length;w++) {
					if( words[w] == '' ) continue;
					count_matches = count_matches + highlightWord(doc.getElementsByTagName("body")[0],words[w],doc);
					if( p % 2 == 0 ) searchhi_string = searchhi_string + ' ' + words[w];
					else searchhi_string = searchhi_string + ' "' + words[w] + '"';
                		}
			}

	        }
	}
     return count_matches;
}

// Everything form this point on is modified to allow for highlighting
// of terms found in the REQUEST URI
function localSearchHighlight(searchStr, tryQ, doc) {
     tryQ = typeof(tryQ) != 'undefined' ? tryQ : 0;
     doc = typeof(doc) != 'undefined' ? doc : document;
	if (!doc.createElement) return 0;
     if (searchStr == '') return 0;
     count_matches = 0;
	if (searchStr.indexOf('?') == -1) qs = searchStr.substr(0);
	else qs = searchStr.substr(1);
	qsa = qs.split('&');
	for (i=0;i<qsa.length;i++) {
		qsip = qsa[i].split('=');
	        if (qsip.length == 1) continue;
        	if (qsip[0] == 'h' || ( tryQ && ( qsip[0] == 'q' || qsip[0] == 'p' ) ) ) { // be careful about ghost highlights
			// Trim leading and trailing spaces after unescaping
			qsip[1] = unescape(qsip[1]).replace(/^\s+|\s+$/g, "");
			if( qsip[1] == '' ) continue;
                        phrases = qsip[1].replace(/\+/g,' ').split(/\"/);
			// Use this next line if you would like to force the script to always
			// search for phrases. See below as well!!!
			//phrases = new Array(); phrases[0] = ''; phrases[1] = qsip[1].replace(/\+/g,' ');
			for(p=0;p<phrases.length;p++) {
			        phrases[p] = unescape(phrases[p]).replace(/^\s+|\s+$/g, "");
				if( phrases[p] == '' ) continue;
				if( p % 2 == 0 ) words = phrases[p].replace(/([+,()]|%(29|28)|\W+(AND|OR)\W+)/g,' ').split(/\s+/);
				else { words=Array(1); words[0] = phrases[p]; }
	                	for (w=0;w<words.length;w++) {
					if( words[w] == '' ) continue;
					count_matches = count_matches + highlightWord(doc.getElementsByTagName("body")[0],words[w],doc);
					if( p % 2 == 0 ) searchhi_string = searchhi_string + ' ' + words[w];
					else searchhi_string = searchhi_string + ' "' + words[w] + '"';
					// As before, use this next line if forcing phrase searching
					//else searchhi_string = searchhi_string + ' ' + words[w];
                		}
			}
	        }
	}
     return count_matches;
}

function postSearchHighlight(doc) {
        doc = typeof(doc) != 'undefined' ? doc : document;
        // Trim any leading or trailing space
        // (this is an overkill way of getting rid of the leading
        //  space that always is present in searchhi_string)
        searchhi_string = searchhi_string.replace(/^\s+|\s+$/g, "");

        // In MSIE, sometimes the dynamic generation of the spans
        // for the highlighting takes the anchor out of focus.
        // Here, we put it back in focus.
        if( doc.location.hash.length > 1 ) doc.location.hash = doc.location.hash;
}

function SearchHighlight(doc,loc) {
     // This logic should allow pages to use themselves as search
     // engines while not ghosting old searches on current results.
     doc = typeof(doc) != 'undefined' ? doc : document;
     loc = typeof(loc) != 'undefined' ? loc : doc.location;
     count_matches = 0;
     if( doc.createElement ) {
          var docrefpage = doc.referrer.split('?',2);
          var locrefpage = loc.href.split('?',1);

          // Check to see if the referrer looks like it has search terms
          //   In the special case when the referrer *IS* this page,
          //   ignore the referrer.
          if( ( docrefpage[0].toUpperCase() != locrefpage[0].toUpperCase() )
              &&
              ( ( docrefpage[1] && docrefpage[1].match(/(^|&)(p=Q&ts=e&|query=|key=|keywords=|searchfor=|qt=|q=|p=|w=|s=)/) )
                || doc.referrer.match(/\/search\/web\//) ) ) 
          {
               // Look to location (via "h" field) *AND* referrer
	          googleSearchHighlight(doc);
	          count_matches = count_matches + localSearchHighlight(loc.search, 0, doc);
          } else {
               // Look to location *ONLY* for highlighting
               var locsearch = loc.search;
               if( locsearch.indexOf('?') == -1 ) {
                    // Found no GET string, so look to pathname in
                    // last effort to match something
                    locsearch = locsearch.replace(/\/search\//,'?search&q='); // Most WebCrawler searches
               }
               else
               {
                    locsearch = locsearch.replace(/(\?|&)highlight=/,"$1h=");
               }
	          count_matches = count_matches + localSearchHighlight(locsearch, 1, doc);
          }
          postSearchHighlight(doc);
     }
     return count_matches;
}

function SmartHighlight(doc,loc)
{
	// This function is like SearchHighlight(doc)
	// but it detects a page refresh and toggles highlighting
	// on each refresh. This gives a quick way to turn off
	// highlighting (and quickly turn it on after).

     doc = typeof(doc) != 'undefined' ? doc : document;
     loc = typeof(loc) != 'undefined' ? loc : doc.location;

	var today = new Date();
	var now = today.getUTCSeconds();

	var cookie = doc.cookie;
	var cookieArray = cookie.split('; ');

	// Get timestamp stored in cookie
	for (var loop=0; loop < cookieArray.length; loop++){
		var nameValue = cookieArray[loop].split("=");
		if (nameValue[0].toString() == 'SHTS'){
			var cookieTime = parseInt( nameValue[1] );
		}
		else if (nameValue[0].toString() == 'SHTSP'){
			var cookieName = nameValue[1];
		}
	}

	// If we got a cookie, the cookie is from this page,
	// and the cookie's time is very close to now, then
	// this must be a page refresh (or very similar)
	// so we don't want to highlight. (the 5 second threshold
	// may need to be adjusted for slower browsers/pages/etc.)
	if( cookieName &&
		cookieTime &&
		cookieName == escape(loc.href) && 
		Math.abs(now - cookieTime) < 5 )
	{
		// Refresh detected, so don't highlight

		// Disable refresh detection for this run;
		// this is what allows us to toggle the highlighting
		// back *ON* on the next refresh
		searchhi_unl = 0;
	}
	else
	{
		// This is not a refresh, so highlight
		return SearchHighlight(doc);
	}
     return 0;

}

function SmartHLUnload(doc)
{
     doc = typeof(doc) != 'undefined' ? doc : document;
     loc = typeof(loc) != 'undefined' ? loc : doc.location;

	if( searchhi_unl > 0 )
	{
		// Turn refresh detection on so that if this
		// page gets quickly loaded, we know it's a refresh
		var today = new Date();
		var now = today.getUTCSeconds();
		doc.cookie = 'SHTS=' + now + ';';
		doc.cookie = 'SHTSP=' + escape(loc.href) + ';';
	}
	else
	{
		// Refresh detection has been disabled
		doc.cookie = 'SHTS=;';
		doc.cookie = 'SHTSP=;';
	}
}

function NotRefreshHL() 
{
	// This is not a refresh. It's probably a submit
	// with the same search string, so disable refresh
	// detection on this go around.
	searchhi_unl = 0;
	return true;
}

// By default, turn refresh detection on
var searchhi_unl = 1;

// window.onload = SearchHighlight;
// window.onload = SmartHighlight;
// window.onunload = SmartHLUnload;
