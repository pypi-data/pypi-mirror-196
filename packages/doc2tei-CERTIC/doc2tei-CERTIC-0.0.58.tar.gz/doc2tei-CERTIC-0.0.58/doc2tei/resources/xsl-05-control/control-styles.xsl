<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="#all">
    
<xsl:output method="xml" encoding="UTF-8" indent="no"/>

<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:variable name="source">
    <xsl:value-of select="//*:application[starts-with(@ident,'circe')]/@ident"/>
</xsl:variable>    
<!--
<xsl:template match="text:*">
    <p>
        <xsl:attribute name="rend" select="@text:style-name"/>
        <ERROR><xsl:text>Unknown style "</xsl:text><xsl:value-of select="@text:style-name"/><xsl:text>" converted to p element.</xsl:text></ERROR>
        <xsl:apply-templates/>
    </p>
</xsl:template>
-->
    
<xsl:template match="*[ancestor::*:text]">
<!--
    <xsl:comment><xsl:value-of select="namespace-uri()"/></xsl:comment>%
    <xsl:comment><xsl:value-of select="local-name()"/></xsl:comment>%
    <xsl:comment><xsl:value-of select="name()"/></xsl:comment>%
-->
    <xsl:choose>
        <xsl:when test="contains(name(),'text:')">
            <p>
                <xsl:if test="$source='circe-Metopes'">
                    <xsl:attribute name="rend">
                        <xsl:value-of select="@text:style-name"/>
                    </xsl:attribute>
                </xsl:if>     
                <ERROR><xsl:text>ERROR: Unknown style "</xsl:text><xsl:value-of select="@text:style-name"/><xsl:text>" converted to p element.</xsl:text></ERROR>
                <xsl:apply-templates/>
            </p>
        </xsl:when>
        <xsl:otherwise>
            <xsl:choose>
                <xsl:when test="./local-name()='div' or (./local-name()='cit' and not(ancestor::*:cit)) or ./local-name()='figure' or (./local-name()='bibl' and ancestor::*:back)">
<!-- (./local-name()='div' and not(ancestor::*:front)) -->
                    <xsl:variable name="currentElementName">
                        <xsl:value-of select="name(.)"/>
                    </xsl:variable>
<!-- <xsl:when test="($currentElementName='div' and ./@type='abstract')"/> -->
                    <xsl:element name="{$currentElementName}">
                        <xsl:copy-of select="@*"/>
                        <xsl:attribute name="xml:id">
                            <xsl:choose>
                                <xsl:when test="@xml:id">
                                    <xsl:copy-of select="@xml:id"/>
                                </xsl:when>
                                <xsl:when test="$currentElementName='bibl'">
                                    <xsl:value-of select="$currentElementName"/><xsl:number count="*[local-name()=$currentElementName]" from="*:back" level="any"/>
                                </xsl:when>
                                <xsl:when test="($currentElementName='div' and ./@type='bibliography') or ($currentElementName='div' and ./@type='appendix')">
                                    <xsl:value-of select="@type"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="$currentElementName"/><xsl:number count="*[local-name()=$currentElementName]" from="*:text" level="any"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:attribute>
                        <xsl:apply-templates/>
                    </xsl:element>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:variable name="currentElementName">
                            <xsl:value-of select="name(.)"/>
                        </xsl:variable>
                        <xsl:element name="{$currentElementName}">
                            <xsl:copy-of select="@*"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:otherwise>
            </xsl:choose>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
    
</xsl:stylesheet>