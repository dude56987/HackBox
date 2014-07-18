// ==UserScript==
// @name         FlashBlock Wannabe
// @namespace    MonkeeSage
// @description  Act like FlashBlock for Firefox.
// @version      0.1.1
// @copyright    2009, Jordan Callicoat
// @license      MIT
// @include      *
// ==/UserScript==

/**************************************************************************
 **************************************************************************/
// README (no, really, do it)
//
// A user script for Opera 9, Midori, GreaseMonkey, or other DOM2 / CSS2
// browsers. It tries to provide all the main features of FlashBlock, as
// well as a few small extras. This script works as a stand-alone user
// script, though it is recommended that you use a custom stylesheet also.
// The CSS rules are found in the file FlashBlock.css (located in the same
// directory as this file). These are the same rules written directly
// to the head of the document by this script, the only difference is
// that custom stylesheets can be loaded before user scripts in some
// implementations, and the faster the style rules get parsed and applied,
// the less chance the flash element has to start loading.
//
// The following is a list of features:
//
// * Blocks everything FlashBlock does (though unlike FlashBlock, it uses the
//   same icon for all blocked media types)
//
// * Listens for modifications to the DOM (element insertion and deletion,
//   attribute changes) to catch several cases not handled by FlashBlock at
//   the time of this writing. For example, if a script tries to write a flash
//   object three seconds after a link is clicked, it will be detected and
//   blocked, just as if it were statically embeded in the markup. Or if a Bad
//   Person(TM) creates an innocent image in an object tag (yes, the spec allows
//   it), but changes the src attribute to load some swf on mouseover, it will
//   be detected and blocked. (NOTE: WebKit doesn't hear DOMAttrModified events
//   yet, so the second use case mentioned above will not work in Midori, Arora,
//   or Safari. However, the upshot is that the style rules will still block
//   the flash element--no sneaky flash loaders!--, there just won't be a
//   placeholder for it.)
//   PREFORMANCE NOTE: This feature could, in theory, cause a noticable
//   preformace hit. Every time a page is modified (be it through document.write,
//   or DOM manipulation methods--excluding our own insertion of placeholders),
//   the blocking mechanism will jump through its hoops looking for new items to
//   block. Practically speaking, you will probably never even notice it--even
//   on pages with lots of dynamic content. But, it case you do, or if you just
//   wish to have the standard FlashBlock behavior, you can disable listening to
//   DOM mutation events by setting __FLASHBLOCK_LISTEN_TO_DOM to false below.
//
// * Keeps a vague idea of a single item queue (more like an activity flag). If 
//   a block operation is running and another item requires a block, the current
//   operation completes and three seconds later a new block operation is started.
//   Three seconds is a long time, relatively speaking, but this interval
//   represents the time elapsed between checking when blocking is needed--even
//   when nothing has happened. I.E., this check runs every three seconds,
//   unconditionally (though it's just a simple compare operation, not the whole
//   blocking mechanism). So three seconds seems like a good interval. If you
//   wish to disable queued events (NOT A GOOD IDEA!), then set
//   __FLASHBLOCK_ENABLE_QUEUES to false below.
//
// * Wraps the placeholder in a link (with a title attribute) so the href
//   can be copied, it can be opened in a new window, has a nice tooltip, &c.
//   (There is no way to generate a custom context menu like FlashBlock has;
//   for most cases, a simple link context menu will suffice.)
//
// * The placeholder element tries to keep the same layout as the blocked element.
//   Pageflow is usually uneffected, as style rules are generally applied to the
//   containing element (p, div, tr), not to the object / embed element directly.
//
// * Sites can be whitelisted or blacklisted using the @include and @exclude
//   directives in the UserScript preamble above (not possible to provide a
//   GUI for this in JavaScript; a GUI may be provided by the user script
//   mechanism--GreaseMonkey provides one, for example). There is no per-object
//   blocking like FlashBlock. If you need very-fine-grained control, you
//   might consider installing Privoxy (www.privoxy.org) and writing custom rules
//   for the object(s) in question.
//
// * Uses 100% compatible DOM2 / CSS2. No reliance on implementation details of
//   various UAs. No pseudo-properties and such. Just good, clean, standards-
//   compliant code.
//
// Differences from FlashBlock (apart from those mentioned above):
//
// * A notable difference from FlashBlock is that we don't currently block
//   flash objects when they are loaded directly as the window location. In other
//   words, if you directly enter the swf address in the URL bar, we don't try
//   to block the generated flash element (which is either directly [or a child]
//   embed element in most UAs). This may be supported in future versions.
//
/**************************************************************************
 **************************************************************************/

// ERRATA:
// Known broken sites (broken in Opera or WebKit, works in FF):
// * http://www.doodoo.ru/games/5085-cavern-escape.html
//   Doesn't work in WebKit. But loading the iframe directly does work...
//   http://www.doodoo.ru/games/flashgames/200902/cavernescape/index.html
//   ...hmm.


// user configuration options
var __FLASHBLOCK_PRETTY_BORDER = true;
var __FLASHBLOCK_LISTEN_TO_DOM = true;
var __FLASHBLOCK_ENABLE_QUEUES = true;


/*******************************************
 * don't modify anything beyond this point *
 *******************************************/

// useless 'til querySelectorAll is supported by more UAs
//var __FLASHBLOCK_DATA = {
//	selectors : [
//		'object[classid$=":D27CDB6E-AE6D-11cf-96B8-444553540000"]',
//		'object[classid$=":166B1BCA-3F9C-11CF-8075-444553540000"]',
//		'object[classid$=":15B782AF-55D8-11D1-B477-006097098764"]',
//		'object[classid$=":32C73088-76AE-40F7-AC40-81F62CB2C1DA"]',

//		'object[codebase*="swflash.cab"]',
//		'object[codebase*="sw.cab"]',
//		'object[codebase*="awswaxf.cab"]',

//		'object[type="application/x-shockwave-flash"]',
//		'embed[type="application/x-shockwave-flash"]',
//		'iframe[type="application/x-shockwave-flash"]',
//		'object[type="application/x-director"]',
//		'embed[type="application/x-director"]',
//		'object[type="application/x-authorware-map"]',
//		'embed[type="application/x-authorware-map"]',
//		'object[type="application/ag-plugin"]',
//		'embed[type="application/ag-plugin"]',

//		'object[data*=".swf"]',
//		'object[data*=".dcr"]',
//		'object[data*=".aam"]',

//		'object[src*=".swf"]',
//		'embed[src*=".swf"]',
//		'iframe[src*=".swf"]',
//		'object[src*=".dcr"]',
//		'embed[src*=".dcr"]',
//		'object[src*=".aam"]',
//		'embed[src*=".aam"]',

//		'object[source*=".xaml"]',
//		'embed[source*=".xaml"]',
//		'object[sourceelement*="xaml"]
//	]
//};

/*******************************************************
 *******************************************************
 * write CSS directly into page as quickly as possible *
 *******************************************************
 *******************************************************/
(function ()
{

	var CSS_STRING = '/* Borrowed these selectors and icons from FlashBlock */\n\
\n\
object[classid$=":D27CDB6E-AE6D-11cf-96B8-444553540000"],\n\
object[classid$=":166B1BCA-3F9C-11CF-8075-444553540000"],\n\
object[classid$=":15B782AF-55D8-11D1-B477-006097098764"],\n\
object[classid$=":32C73088-76AE-40F7-AC40-81F62CB2C1DA"],\n\
\n\
object[codebase*="swflash.cab"],\n\
object[codebase*="sw.cab"],\n\
object[codebase*="awswaxf.cab"],\n\
\n\
object[type="application/x-shockwave-flash"],\n\
embed[type="application/x-shockwave-flash"],\n\
iframe[type="application/x-shockwave-flash"],\n\
object[type="application/x-director"],\n\
embed[type="application/x-director"],\n\
object[type="application/x-authorware-map"],\n\
embed[type="application/x-authorware-map"],\n\
object[type="application/ag-plugin"],\n\
embed[type="application/ag-plugin"],\n\
\n\
object[data*=".swf"],\n\
object[data*=".dcr"],\n\
object[data*=".aam"],\n\
\n\
object[src*=".swf"],\n\
embed[src*=".swf"],\n\
iframe[src*=".swf"],\n\
object[src*=".dcr"],\n\
embed[src*=".dcr"],\n\
object[src*=".aam"],\n\
embed[src*=".aam"],\n\
\n\
object[source*=".xaml"],\n\
embed[source*=".xaml"],\n\
object[sourceelement*="xaml"]\n\
{\n\
	display: none;\n\
}\n\
\n\
a.flashBlocked,\n\
a.flashBlocked:hover,\n\
a.flashBlocked:active,\n\
a.flashBlocked:visited\n\
{\n\
	text-decoration: none !important;\n\
	color: transparent !important;\n\
	border: none !important;\n\
}\n\
\n\
div.flashBlocked,\n\
iframe.flashBlocked\n\
{\n\
	display: inline-block !important;\n\
	border: 1px solid #DDDDDD !important;\n\
	min-width: 40px !important;\n\
	min-height: 40px !important;\n\
	background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAqCAYAAADFw8lbAAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6AAAdTAAAOpgAAA6lwAAF2+XqZnUAAANkklEQVR4nGL8//8/w1AAAAHEQqF+ZiAWyKntl3/9/oPkp09fhIF8Rqjcfz4+njdiYhIvJtdl3gPyPwHxP3ItAgggRjJDVNw3qdTp7qNnHr/+/FXm4ODgFeDh4eBgY2NBdui7Tx9//wCC799/fubkZL+nLCe1ffO87j1AuTekWggQQKQ6VNrIJznv05evVhIiImLSEsL8fHwCHHx8fKw8XGxM7CxMTMiKf/759+/r50//Pn799fvz27ffbz19/un9+48vBQX5j53bMreHFAcDBBCxDmXxjCuOunH3YbK8lJicsoKigKSECIcgvwCLgCAfEx8XFyMbOzvYPDR9/3/9/Mnw6du3/x/ef/r3/uOHP/cePv9x497dd89ePH9kqqc9ExjCq4Hq/hJyAEAAEeNQERWHiKnA6NUx0NISV5AW5REXF2eVEBZk5OPjYmSHOJCBg4UVpwE//vxm+PrpO8O3nz/+gxz98uWL31duPPxy8MTZ55xcrJfvHFiRwQBJwzgBQAARcqiUtFnwHEU5SU1DPW1RBSkJDjlpCSYhfj5GDg5ILHMwMzMwszEzsDNgz5fffv2E+FaEj4GVhQ0Yuj8ZPnz89v/1q+d/D5y7+WPngcOv37x5de3FmW0JDHiSAkAA4XOoBNCR8zVV5LX1gY7UUpRgk5GRYYKFoAA3JAQ5gPmHnYkNqwE///1iEBcSYACmSYbr1x8yHD57huH8pZsM7z9+YxDk52Lwdnf4d/rq3Z+bdx14DUwKV4GOjcPlWIAAwlU8cShah8wCOlIL5EgDDWU2MVFBJh5ONmAIMjFw80AcC3IgExskWYJCCx0oCgsxfPz2l6Ft2lKGdZu3Mjx5/YHhByMbw29mdoZ/bOwMWnoGTJ52VuzADCd64vx1LWDAzH56am04UOsvdLMAAgibQxmBObsBGAoaQEeKAB3JLiUmCo5qbpBDoSGI7EBmVhYGNkbUmAGF4sOnLxhyKloY9h4/z8AmKMrALaHEIMLFC5b//u0zw6XHrxj8HI2YjA102f8zc4i++/BeE2h3PbBEqEZ3FEAAMaELAAtvQ2DR52xpaCAGjG6sjmTnYgc7kIOTCyjOAcxILAxMzKwMwLISjEGOBJYQDBGZ5WBHCqtqMogoajJwQh0JAh+//GR48uo12BxFaWkmLVUFdidLE/GXrz44l7RO1UJ3F0AAoTuUdd/xMwUGWtpSykoKXBKiUkzYHAkCMAeyszHBMbBkAOOX7z4xlDZ0M5y4dptBUMOQgV1QAljAMYMxKCRfvHrDwMbBzsDFwwWODQFeFgYZCREmdXV1Ln0dTZkNuw83MkBqPTgACCCUqE8u7bYQEhDUU1WR5ZOVEGHm5uNkBKVJZEeCDIY5EARADkMH05ZsBIekjKoWUA8wFP9Aisl3nz4z6KpKM8Q5mDEYaykA9XIx/P7yFVhi/GUQ4eFk/CElwWKip8H/4NF9ldSqfvPZbYXHYGYCBBCyQ5nOX78RYqipISIiJMwOLCOZQGUjF1KaJMaRR89dZ1i6fCU4TXLxiwBFIGn39YcvDMH2JgyNSX4MnMDi7Ovnb2DxL79/Ac3nBNrzi4Gf7x+TvKwku6aGuujxcxfjgdLHYQYABBBy1EsCsYmMrAQPsDBnBudwYCwDMynYkaC0BMowTEDHw6IYG1i+fgfD3dfvGERklBj+MrGA8dMXb8GO7MoIZPgHrKlevvvA8BsYyCAMK9qADQVwkSciKMisqSjLA8wnoHQqDDMXIIDgDg3PqdeXEJMUgoYmI6ggBxXiIINgOZuFnQur42Dg7MVbDDv27GXgFxRjAOYcsNiLZy8ZgG0CcEgy/IaELg8rG7iMRQcg+3g42BmBNR8bsC0hFJXXZgSTAwgguENfv32jDjSQm4uTnRlYqIPLHlhogn0MjHJWpr8MvFy4q8qDx0/AQxME3gFD7tuHtww5PnZg/svPH8FRDQtJdMeCQpWbi4NRgIeLRVxCjPvF66caMDmAAIKlUZZfv344A1tBnMAGBhMr039ItQiNFlBoQgzCHt0g8OzlO4ZNe08APQeMLVZ2sCO/f/vEwM7HwzBlyyGG+SvWMvz/8ovh/9c3DH6BXgylBRkMT58/wzAHlNw42NmZJAV5Oe4/eKgKDcx/AAEEdygDIycnsKnGAmwFMcKKIxBATpsMf4D1Ngs7Vofevv+A4dT5iwycIjLg3A1yJFzu0lVgk+MTw//vvxgYv35kUDd/w8DLBmlDY0sCXOwcjOzcfKzAtq4aNDB/AQQQzKEgV7Ows3EyAl3MCEubyAAU7QwsuEN0776jDN/fvGPgkFIGO/L3b0TLjYmfj4EBhEFB8/ETMMOIAFtUmG0MkJ3/wQ5hYgS1b0HWQt3GABBAyLmekQGzPcnw+88vcK2DD4Cqyumzl4DZzEzsKI5EBv++fweGzR+GX3//oDgOhtEAIxsLM9w9AAGEXI7+Z4AVesiG//rP8PX7D2DU8zLgCs+d+48yvHlwj4FR35bhxz9glLJyMPz79B7YDnoLjm4U8PUlw+e3xnjTO5J74H0sgACCORQk8BtE/2H4//8nwx9GDgaEDz99+czwE9iO/AysmUBVJzqYv2oTMGh4GZj4BCGGvXnFAMyVDFFxAQzADMrw4+s3hMd/fmYwMdZnAHZJsLoOaDfYkX9/g6szkC/B0QMQQDCH/mJj/f/129fPvxmwhCosWn5++QDECHEBXiGGY+fPMJzYdRjYxFaGCP7+wfD/5RuGCO8gBmDvEyz0/dMPFPN+/f0BLvRxtWN//PwL7Gf9+MnO9Oc0kAt2OUAAwUOUnZVj0/sPX/S/ff/y98dPfmZ+NmB6AlZtKADKB+VUsCWsjAz1E+aBxZjFxcCO/AcsRxkFBRgCPayBZS8jw5Nn77A6BlS/AxMthh1/f/1lAPaz/r598/6HgIDIXVjAAQQQPDMpSAhfffH+/edvP37/AfZx/v/4xcyADkAOBGFQzaKoKMnQP30Rw9n9wLJTSRuu5v/7DwwedsYMpoY6DC9fvwcX8OgYnNdADkRzJMjsH3//gvpVf1+9efMF6KbrMDmAAII7dHpX1d2P7z4A266ffgI7Yv+gaQVuAAiI8/IzSIqKMvAK8DPUtU1maO6axgBsn0GKH1BovHwFLIZ4GBJDvRn4udgY3n/7iRqK2HM3wpNAa758//UP2Pn78e7Tx7dAN92EyQEEEHKuf/vv/89ND569UJCSFOYW/snHxMH2C1w8gEIQBI5evsZw6/YdhtXb9jKcOHQK2GMTZGDkkYAUOyDw8QtDUlIQg5u1PsObV+/hjiMWADuC/z99+vbn2p2nn/k42bcxIPVMAQII2aH/1GWlD9198DRCTUmeX0jgCzMHOw8zqPCXUZZk2LzrCENSXCrDG2C+YOQRY2CUUmFgYEOUr/8fP2cwNlNkKM2KAfM/f/0FrruJBR9/fGP48PX3/8cv3vx48OjRSwtD7a0MSBkbIIBQWvjAoL7w4/v7VbfuPQSmgY9/vn7/9R+cBIBVJ9N/oAs5+RgYFTQZmGRl4NHN8Os32JFSylIMnbXVDBrAtPvs6WuSHPnjxy8GkF3vPn76fe7y9ffAwndzT3X2LWQ1AAGE3rn7baSjteXC1dt+kmKiPFycPPxAMWZgT5KRh18IrOA/sB7/C8SIoPjCYKCrwtDfU83gYKIB7haTAkDpHxTlHz78+Hv55t3P127dfORjZbCUAW30BCCAMDp3QJ/c4Gf/M+HslWvPHj178e3Nh+9/n7/9yCAuKszALyEKdhgjsDEsys3BYCAnwZCdFcawbn4Xg4OBItyRxIYmyJFfgZ08YJT/u/fs+dd9R048VRTlntBUlXsfXS1AAOEagOB0CM3KVVZQTDTQ15ZWkpLkUpYXYj50/AzD03ffGICNawZFSQEGbSVFcDEFqmVevPhAkiNB0f3x5x9gLfPj34PnL76t3br/6fs3j5cd37SwgwFSS6IAgADCN1LCD3RsJtCxCUDHSoIca2KgzAwsdhhBBTkIvH/3HdwYJgf8+PXnPzAk/959+BTkyOdAR64EOrILKPUVm3qAAMI3kPvxwOpp04GO/f/z7//YXz9+SgHFeKQl+ViAvUd4qwZWdIEArNEEK3eRiyZYTwEK/n/4/OfPucu3v2zbvf/Z1y9v1wAd2Y3LkSAAEEDEjObx+cbmBPxlFcg10laW0dZQ5tNUkmYTExJk5uXlZQS3U4kEP3/9+w9M739v3n/+69Cp859Onjn/WJCTYfLmxVPW4XMkCAAEELHjo6zZJbWG9159axIUEJZXUZIT1lVX5lZVEGNTlJYEllTwEMYYH4XRwK7Kv8t3Hv86dvbS19MXbr799PH5A31FqbqpPc3nGIgYHwUIIFJHnPljMkqs3n77X8TFxy8lJSYqqCAlwSUnLcEiJS7ADOzCICeL/x8+fvvz8t3Hv8DS4zewbP4OrEzeA8vpZ1L8nH1LZvSABheITuAAAUTOGD7IIXzAENb8+OV7+cdfjKC+NzcbFy/QnRzc7MyM4E4VMF3//P7rx9df3z5/+f7j71dgkfdWQpi/CxiCoIYGqGokyWKAACJ3sgEGQHUoqAPPX1zVIPzj198SKB8EvnGwMff0tjWAxjtBFT+ohYJR7BALAAKIUofSDQAEEEbNNFgBQIABABWRKc05F+/jAAAAAElFTkSuQmCC") no-repeat center !important;\n\
}\n\
\n\
div.flashBlocked:hover,\n\
iframe.flashBlocked:hover\n\
{\n\
	background-image: url("data:image/png;base64,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") !important;\n\
}';


	function _insert_css (event)
	{
		if (!document.getElementById ("flashblock-style"))
		{
			var head;
			if ((head = document.getElementsByTagName ("head")[0]))
			{
				var style = document.createElement ("style");
				style.setAttribute("type", "text/css");
				style.setAttribute("id", "flashblock-style");
				style.appendChild (document.createTextNode (CSS_STRING));
				head.appendChild (style);
			}
			else
			{
				if (event) // page loaded and no head element...
				           // really? seriously!?? what year is this? 1994?
				{
					head = document.createElement ("head");
					document.documentElement.insertBefore (head, document.body);
				}
				window.setTimeout (function () { _insert_css (); }, 300);
			}
		}
	}

	_insert_css ();
	
	// make sure our stylesheet is loaded by the time the DOM is ready
	window.addEventListener ("load", function () { _insert_css (); }, true);

})();


// main function
// keeping it anonymous makes it harder to circumvent the blocking process
(function (detect_border_color, listen_to_dom, queue_events)
{

	// keep an explicit reference to ourself
	var self = this;


/*****************************************************************************
 *
 * api
 *
 */
	self._get_href = function (element)
	{
		if (element.hasAttribute ("src"))
		{
			return element.getAttribute ("src");
		}
		else if (element.hasAttribute ("data"))
		{
			return element.getAttribute ("data");
		}
		else
		{
			for (var i = 0 ; i < element.childNodes.length ; ++i)
			{
				var node = element.childNodes[i];
				if (node.nodeName == "PARAM")
				{
					var attr_name = node.getAttribute ("name").toLowerCase ();
				    if (attr_name == "src" || attr_name == "movie")
					{
						return node.getAttribute ("value");
					}
				}
			}
			return "";
		}
	}

	self._get_border_color = function (element)
	{
		var style, color;
		if ((style = window.getComputedStyle (element, null)))
			color = style.backgroundColor;

		while ((element = element.parentNode) &&
		       (color == "rgba(0, 0, 0, 0)" || color == "transparent"))
		{
			try
			{
				if ((style = window.getComputedStyle (element, null)))
					color = style.backgroundColor;
			}
			catch (e)
			{
				// foobar'd
			}
		}

		if (color != "rgba(0, 0, 0, 0)"   &&
		    color != "transparent"        &&
		    color != "rgb(0, 0, 0)"       &&
		    color != "black"              &&
		    color != "#000000"            &&
		    color != "rgb(255, 255, 255)" &&
		    color != "white"              &&
		    color != "#ffffff")
		{

			var rgb = [];
			if (color[0] == "#")
			{
				rgb[0] = parseInt (color.slice (1, 3), 16);
				rgb[1] = parseInt (color.slice (3, 5), 16);
				rgb[2] = parseInt (color.slice (5, 7), 16);
			}
			else
			{
				rgb = color.slice (4, -1).split (",");
				rgb[0]  = parseInt (rgb[0], 10);
				rgb[1]  = parseInt (rgb[1], 10);
				rgb[2]  = parseInt (rgb[2], 10);
			}

			var i;
			if ((rgb[0] + rgb[1] + rgb[2]) > 459) // 3/5 of #FFFFFF
			{ 
				for (i = 0 ; i < 3 ; ++i)
				{
					rgb[i] -= Math.round (rgb[i] / 0.75);
					if (rgb[i] < 0) rgb[i] = 255 + rgb[i];
				}
			}
			else
			{
				for (i = 0 ; i < 3 ; ++i)
				{
					rgb[i] = rgb[i] + Math.round (rgb[i] * 0.75);
					if (rgb[i] > 255) rgb[i] = 255 - (rgb[i] - 255);
				}
			}

			return "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
		}

		return null;
	}

	self._get_width_height = function (element)
	{
		var width_height = ["40px", "40px"];
		var style = window.getComputedStyle (element, null);
		if (style.width != "0px" && style.height != "0px" &&
		    style.width != "auto" && style.height != "auto")
		{
			width_height[0] = parseInt (style.width.slice (0, -2)) - 2 + "px";
			width_height[1] = parseInt (style.height.slice (0, -2)) - 2 + "px";
		}
		else
		{
			element.style.display = "inline-block";
			width_height[0]       = element.offsetWidth  - 2 + "px";
			width_height[1]       = element.offsetHeight - 2 + "px";
			element.style.display = "none";
			if (width_height[0] == "-2px" || width_height[1] == "-2px")
			{
				while ((element = element.parentNode))
				{
					if (element.offsetWidth > 0 && element.offsetHeight > 0)
					{
						width_height[0] = element.offsetWidth  - 2 + "px";
						width_height[1] = element.offsetHeight - 2 + "px";
						break;
					}
				}
			}
		}
		return width_height;
	}

	self._insert_placeholder = function (element)
	{

		var href         = self._get_href (element);
		var width_height = self._get_width_height (element);

		var link = document.createElement ("a");
		link.setAttribute ("class", "flashBlocked");
		link.setAttribute ("href", href);
		link.setAttribute ("title", href);

  		var div = document.createElement ("div");
  		div.setAttribute ("class", "flashBlocked");
		div.style.width  = width_height[0];
  		div.style.height = width_height[1];

		// set a nice border color based on container background color...
		if (self.__border)
		{
			var color;
			if ((color = self._get_border_color (element)))
			{
				div.style.border = "1px solid " + color + " !important";
			}
		}

  		// we only want to make a placeholder once...
  		element.setAttribute ("blocked", true);

		link.appendChild (div);
		element.parentNode.insertBefore (link, element);

		link.addEventListener (
			"click",
			function (event)
			{
				event.preventDefault ();
				link.blur ();
				if (self.__linux && link.href.indexOf (".dcr") > -1)
				{
					alert ("No Director plugin for your platform, sorry... :(");
					return false;
				}
				link.style.display    = "none";
				element.style.display = "inline-block";
				// opera uses the embed element so we need to display that as well
				if (element.nodeName == "OBJECT")
				{
					var node, i;
					for (i = 0 ; node = element.childNodes[i] ; ++i)
					{
						if (node.nodeName == "EMBED" || node.nodeName == "OBJECT")
						{
							node.style.display = "inline-block";
						}
					}
				}
				return false; 
			},
			true
		);

	}

	self._block_elements = function (elements)
	{
		for (var i = 0 ; i < elements.length ; ++i)
		{
			if (elements[i].parentNode.nodeName != "OBJECT" &&
			    !elements[i].hasAttribute ("blocked"))
			{			
				self._insert_placeholder (elements[i]);
			}
		}
	}

	self._check_select_element = function (element)
	{
		var attrval;

		if (element.hasAttribute ("classid"))
		{
			attrval = element.getAttribute ("classid").toUpperCase ();
			if (attrval == "CLSID:D27CDB6E-AE6D-11CF-96B8-444553540000" ||
			    attrval == "CLSID:166B1BCA-3F9C-11CF-8075-444553540000" ||
			    attrval == "CLSID:15B782AF-55D8-11D1-B477-006097098764" ||
			    attrval == "CLSID:32C73088-76AE-40F7-AC40-81F62CB2C1DA")
			{
				return true;
			}
		}

		if (element.hasAttribute ("codebase"))
		{
			attrval = element.getAttribute ("codebase");
			if (attrval.indexOf ("swflash.cab") > -1 ||
			    attrval.indexOf ("sw.cab") > -1 ||
			    attrval.indexOf ("awswaxf.cab") > -1)
			{
				return true;
			}
		}

		if (element.hasAttribute ("type"))
		{
			attrval = element.getAttribute ("type");
			if (attrval == "application/x-shockwave-flash" ||
			    attrval == "application/x-director" ||
			    attrval == "application/x-authorware-map" ||
			    attrval == "application/ag-plugin")
			{
				return true;
			}
		}

		if (element.hasAttribute ("data") ||
		    element.hasAttribute ("src"))
		{
			attrval = element.getAttribute ("data");
			if (!attrval)
				attrval = element.getAttribute ("src");
			if (attrval.indexOf (".swf") > -1 ||
			    attrval.indexOf (".dcr") > -1 ||
			    attrval.indexOf (".aam") > -1)
			{
				return true;
			}
		}

		if (element.hasAttribute ("source") ||
		    element.hasAttribute ("sourceelement"))
		{
			attrval = element.getAttribute ("source");
			if (!attrval)
				attrval = element.getAttribute ("sourceelement");
			if (attrval.indexOf ("xaml") > -1)
			{
				return true;
			}
		}

		return false;
	}

	self._select_elements = function ()
	{
		var i, selected;
		var elements = [];

		selected = document.getElementsByTagName ("object");
		for (var i = 0 ; i < selected.length ; ++i)
		{
			if (self._check_select_element (selected[i]))
			{
				elements.push (selected[i]);
			}
		}

		selected = document.getElementsByTagName ("embed");
		for (var i = 0 ; i < selected.length ; ++i)
		{
			if (self._check_select_element (selected[i]))
			{
				elements.push (selected[i]);
			}
		}

		selected = document.getElementsByTagName ("iframe");
		for (var i = 0 ; i < selected.length ; ++i)
		{
			if (self._check_select_element (selected[i]))
			{
				elements.push (selected[i]);
			}
		}

		return elements;
	}

	self._block_flash = function (event)
	{
		if (self.__locked || self.__queued)
		{
			self.__queued = true;
		}
		else
		{
			self.__locked = true;
			// don't want to catch our own mutations
			self._remove_dom_listeners ();
			
			// really should be ...
//			var elements = document.querySelectorAll (__FLASHBLOCK_DATA["selectors"].join (","));
//			self._block_elements (elements);

			// but we'll have to do it manually for now...
			self._block_elements (self._select_elements ());

			// restore our listeners if needed
			self._add_dom_listeners ();

			self.__locked = false;
		}
	}

	self._start_queue_listener = function ()
	{
		if (self.__queues)
		{
			if (self.__queued)
			{
				self.__queued = false;
				self._block_flash ();
			}
			// check if queued evey 3 seconds
			window.setTimeout (self._start_queue_listener, 3000);
		}
	}

	self._add_dom_listeners = function ()
	{
		if (document.body == null)
		{
			window.setTimeout (self._add_dom_listeners, 1000);
			return;
		}
		if (self.__listen)
		{
			// XXX: WebKit doesn't hear DOMAttrModified yet:
			// https://bugs.webkit.org/show_bug.cgi?id=8191
			document.body.addEventListener ("DOMAttrModified",
			                                self._block_flash, true);
			document.body.addEventListener ("DOMSubtreeModified",
			                                self._block_flash, true);
		}
	}

	self._remove_dom_listeners = function ()
	{
		if (document.body == null)
		{
			window.setTimeout (self._remove_dom_listeners, 1000);
			return;
		}
		if (self.__listen)
		{
			document.body.removeEventListener ("DOMAttrModified",
			                                   self._block_flash, true);
			document.body.removeEventListener ("DOMSubtreeModified",
			                                   self._block_flash, true);
		}
	}

	self._loaded = function ()
	{
		self._start_queue_listener ();
		self._add_dom_listeners ();
	}

	self._init = function ()
	{
		self._block_flash ();
		self._loaded ();
		window.addEventListener ("load", function (){ self._block_flash (); }, true);
	}


/*****************************************************************************
 *
 * ctor
 *
 */
 	self.__linux  = (navigator.platform.toLowerCase ().indexOf ("linux") > -1 ||
				     navigator.userAgent.toLowerCase ().indexOf ("linux") > -1);
	self.__queues = queue_events;
	self.__listen = listen_to_dom;
	self.__border = detect_border_color;
	self.__locked = false;
	self.__queued = false;
	self._init ();

}) (__FLASHBLOCK_PRETTY_BORDER, __FLASHBLOCK_LISTEN_TO_DOM, __FLASHBLOCK_ENABLE_QUEUES);


