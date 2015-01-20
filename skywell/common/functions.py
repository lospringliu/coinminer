from django.utils.translation import ugettext_lazy as _

superusers_set = set()
superusers_set.add('9818674')
superusers_set.add('2374351836')
#superusers_set.add('674494106')
#superusers_set.add('174316164')
#superusers_set.add('465573094')

def functemp():
	pass

def html_tablize(target,ptabs=2):
	retstring = ''
	if target:
		if type(target) == type(dict()):
			retstring += "\t" * ptabs + "<table>\n"
			for key in target.keys():
				retstring += "\t" * ptabs + "\t<tr>\n"
				retstring += "\t" * ptabs + "\t\t<td>" + str(key) + "</td>\n"
				retstring += "\t" * ptabs + "\t\t<td>\n"
				retstring += html_tablize(target[key],ptabs=ptabs+3)
				retstring += "\t" * ptabs + "\t\t</td>\n"
				retstring += "\t" * ptabs + "\t</tr>\n"
			retstring += "\t" * ptabs + "</table>\n"
		elif type(target) == type(list()):
			retstring += "\t" * ptabs + "<table>\n"
			retstring += "\t" * ptabs + "\t<tr>\n"
			for listitem in target:
				retstring += "\t" * ptabs + "\t\t<td>\n"
				retstring += html_tablize(listitem,ptabs=ptabs+3)
				retstring += "\t" * ptabs + "\t\t</td>\n"
			retstring += "\t" * ptabs + "\t</tr>\n"
			retstring += "\t" * ptabs + "</table>\n"
		else:
			retstring += "\t" * ptabs + "\t" + str(target) + "\n"
	return retstring

def gen_datebar_js(plotid='default plotid',jqplotdata=None,title='default title',varyBarColor=False,barWidth=2,intable=True,width="1000px",height="400px",resizeable=True):
	if resizeable:
		if intable:
			ljqscript = "\t\t<tr><a name=\"" + plotid + "\"></a><td><div id=\"resizable-" + plotid + "\" class=\"ui-widget-content\"><div id=\"" + plotid + "\"></div></div></td></tr>\n"
		else:
			ljqscript = "\t\t<a name=\"" + plotid + "\"></a><div id=\"resizable-" + plotid + "\" class=\"ui-widget-content\"><div id=\"" + plotid + "\"></div></div>\n"
	else:
		if intable:
			ljqscript = "\t\t<tr><a name=\"" + plotid + "\"></a><td><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div></td></tr>\n"
		else:
			ljqscript = "\t\t<a name=\"" + plotid + "\"></a><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div>\n"
	ljqscript += """
		<script type="text/javascript">
		$(document).ready(function(){
	"""
	if resizeable:
		ljqscript += """
			$.jqplot._noToImageButton = true;
			"""
		ljqscript += "$(\"#resizable-%s\").resizable({delay:20, helper:'ui-resizable-helper'});\n" % plotid
		ljqscript += "\t\t\t$(\"#resizable-%s\").bind('resizestop', function(event, ui) {\n" % plotid
		ljqscript += "\t\t\t\t$(\"#%s\").height($(\"#resizable-%s\").height()*0.96);\n" % (plotid, plotid)
		ljqscript += "\t\t\t\t$(\"#%s\").width($(\"#resizable-%s\").width()*0.96);\n" % (plotid,plotid)
		ljqscript += """
			plot.replot( { resetAxes:true } );
		});
			"""
	ljqscript +="		var plot = $.jqplot(\"" + plotid + "\", " + str(jqplotdata) + ",{"
	ljqscript += """
			animate: !$.jqplot.use_excanvas,
			seriesDefaults:{
				renderer:$.jqplot.BarRenderer,
				pointLabels: { show: true },
				rendererOptions: {
				"""
	if varyBarColor:
		ljqscript += "\t\t\t\t\tvaryBarColor: true,\n"
	if barWidth:
		ljqscript += "\t\t\t\t\tbarWidth: %g,\n" % barWidth
	else:
		ljqscript += "\t\t\t\t\tbarWidth: 2,"
	ljqscript += """
					barPadding: 1,
					shadowOffset: 0,
					}
			},
			axes: {
				xaxis: {
					renderer: $.jqplot.DateAxisRenderer,
				}
			},
			cursor:{show: true,zoom:true,showTooltip:'ne'}, 
			"""
	ljqscript += "\t\t\t\ttitle: { text: '" + title + "'}"
	ljqscript += """
		});
	 
	});
	</script>
				"""
	return ljqscript

def gen_donut_js(plotid='default plotid',jqplotdata=None,title='default title',width='1000px',height='400px',intable=True):
	if intable:
		ljqscript = "\t\t<tr><a name=\"" + plotid + "\"></a><td><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div></td></tr>\n"
	else:
		ljqscript = "\t\t<a name=\"" + plotid + "\"></a><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div>\n"
	ljqscript += """
		<script type="text/javascript">
		$(document).ready(function(){
	"""
	ljqscript +="		var plot = $.jqplot('" + plotid + "'," + str(jqplotdata) + ", {"
	ljqscript += """
					grid:
					{
						drawGridLines: false,
						background: '#ffffff',
						shadow: false
					},
					seriesDefaults:
					{
						renderer: $.jqplot.DonutRenderer,
						rendererOptions:
						{
							sliceMargin: 1,
							startAngle: -90,
							dataLabels: 'value',
							showDataLabels: true
						}
					},
					legend: { show: true, location: 'nw'},
	"""
	ljqscript += "\t\t\t\ttitle: { text: '" + title + "'}"
	ljqscript += """
			});
		});</script>
	"""
	return ljqscript

def gen_dateline_js(plotid='default plotid',jqplotdata=None,title='default title',labels=[],forceTickAt0=True,forceTickAt100=True,width='900px',height='600px',showMarker=False,intable=True,fill=[],resizeable=True):
	if resizeable:
		if intable:
			ljqscript = "\t\t<tr><a name=\"" + plotid + "\"></a><td><div id=\"resizable-" + plotid + "\" class=\"ui-widget-content\"><div id=\"" + plotid + "\"></div></div></td></tr>\n"
		else:
			ljqscript = "\t\t<a name=\"" + plotid + "\"></a><div id=\"resizable-" + plotid + "\" class=\"ui-widget-content\"><div id=\"" + plotid + "\"></div></div>\n"
	else:
		if intable:
			ljqscript = "\t\t<tr><a name=\"" + plotid + "\"></a><td><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div></td></tr>\n"
		else:
			ljqscript = "\t\t<a name=\"" + plotid + "\"></a><div id=\"" + plotid + "\" style=\"width:" + width + ";height:" + height + "\"></div>\n"
	ljqscript += """
		<script type="text/javascript">
		$(document).ready(function(){
	"""
	if resizeable:
		ljqscript += """
			$.jqplot._noToImageButton = true;
			"""
		ljqscript += "$(\"#resizable-%s\").resizable({delay:20, helper:'ui-resizable-helper'});\n" % plotid
		ljqscript += "\t\t\t$(\"#resizable-%s\").bind('resizestop', function(event, ui) {\n" % plotid
		ljqscript += "\t\t\t\t$(\"#%s\").height($(\"#resizable-%s\").height()*0.96);\n" % (plotid, plotid)
		ljqscript += "\t\t\t\t$(\"#%s\").width($(\"#resizable-%s\").width()*0.96);\n" % (plotid,plotid)
		ljqscript += """
			plot.replot( { resetAxes:true } );
		});
			"""
	ljqscript += """
			var plot = $.jqplot
			(
	"""
	ljqscript += "\t\t\t'" + plotid + "', " + str(jqplotdata) + ",\n"
	ljqscript += """
			{
				axesDefaults:
				{
					pad: 1
				},
				"""
	if fill:
		ljqscript += "\t\tfillBetween: {series1: %s,series2: %s},\n" % (fill[0],fill[1])
	ljqscript += """
				axes:
				{
					xaxis:
					{
						renderer: $.jqplot.DateAxisRenderer,
						tickRenderer: $.jqplot.CanvasAxisTickRenderer,
						tickOptions:
						{
							showGridline: false,
							fontFamily: 'Tohoma',
							fontSize: '8pt',
							angle: -30
						}
					},
					yaxis:
					{
						rendererOptions:
						{
					"""
	if forceTickAt0:
		ljqscript += """
							forceTickAt0: true,
					"""
	if forceTickAt100:
		ljqscript += """
							forceTickAt100:true
					"""
	ljqscript += """
							}
						}
					},
					cursor:{show: true,zoom:true,showTooltip:'ne'}, 
					grid:
					{
						drawGridLines: false,
						background: '#ffffff',
						shadow: false
					},
					seriesDefaults:
					{
				"""
	if showMarker:
		ljqscript += """
						showMarker: true
					"""
	else:
		ljqscript += """
						showMarker: false
					"""
	ljqscript += """
					},
					legend: { show: true, location: 'nw'},
					series:
					[
					"""
#	if type(labels) == type(list()):
	if labels:
		for label in labels[:len(labels)-1]:
			ljqscript += "\t{ label: '" + label + "'},\n\t\t\t\t\t"
		label = labels[-1]
#		ljqscript += "\t{ label: '" + label + "'},\n\t\t\t\t\t"
#	else:
#			ljqscript += "\t{ label: '" + labels + "'},\n\t\t\t\t\t"
		ljqscript += "\t{ label: '" + label + "'}"
	ljqscript += """
					],
	"""
	ljqscript += "\t\t\t\ttitle: { text: '" + title + "'}"
	ljqscript += """
				}
			);
		}
		);
		</script>
	"""
	return ljqscript
