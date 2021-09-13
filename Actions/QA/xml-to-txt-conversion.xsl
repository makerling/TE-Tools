<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0" exclude-result-prefixes="#all">
      <!--removed namespaces from oxes file, need to add these back for final version xmlns:oxes="http://www.wycliffe.net/scripture/namespace/version_1.1.4"
      xpath-default-namespace="http://www.wycliffe.net/scripture/namespace/version_1.1.4"-->      
    <xsl:output method="text" encoding="UTF-8" indent="no"/>
<xsl:template match="oxes">
    <xsl:for-each select="oxesText/canon/book">
        <xsl:variable name="book" select="@ID" />
        *<xsl:value-of select="$book"/><xsl:text>.0.</xsl:text><xsl:value-of select="titleGroup/title/annotation[1]/@status"/><xsl:for-each select="titleGroup/title/annotation">
		<xsl:if test="notationCategories/category != 'NoNote' and notationCategories/category != 'Misc'">
        		<xsl:text>*</xsl:text><xsl:value-of select="notationQuote/para/span"/>
		</xsl:if>
        </xsl:for-each>
	<xsl:text>*</xsl:text>
	<xsl:value-of select="titleGroup/title/trGroup/tr"/><!--<xsl:text>**</xsl:text>-->
        <xsl:for-each select="section">
            <xsl:variable name="chaptnumb" select="p/chapterStart/@n" />
            <xsl:for-each select="p"><!--puts \p tags but avoids trGroups without verseStart i.e Psalms, or \p nodes where trGroup is the first element, those are done manually below (line 33)-->
                <xsl:if test="verseStart and name(./*[1]) = 'verseStart' or name(./*[1]) = 'verseEnd' or name(./*[1]) = 'chapterStart'">
                    \<xsl:value-of select ="name(.)"/>
                </xsl:if>
                <xsl:for-each select="./*"><!--for loop on each node under \p-->
                    <xsl:variable name="nodePosition2" select="position()" /><!--variable to catch position of nodes under \p-->
                    <xsl:if test="name(.) = 'trGroup' and $nodePosition2 = 1"><!--catching \p nodes where trGroup is first node, i.e a verse spanning multiple paragraphs, or only node-->
                        \p<xsl:text> </xsl:text><xsl:value-of select="tr"/>
                    </xsl:if>
                    <xsl:if test="name(.) = 'verseStart'"><!--finds verse number and the following first sibling of the first trGroup, the rest of the verse gets handles by line 33-->
                        <xsl:variable name="versenumb" select="@ID" /><!--reserving versenum to only process annotation for current verse-->                        
                        *<xsl:value-of select="$book"/><xsl:text>.</xsl:text><xsl:value-of select="$chaptnumb"/><xsl:text>.</xsl:text><xsl:value-of select="@n"/><!--some character needs to be present before argument or it doesn't list each verse on each line-->
                        <xsl:for-each select="../*">
                            <!--versenumb is:<xsl:value-of select="$versenumb"/> oxesRef is:<xsl:value-of select="@oxesRef"/>-->
                            <xsl:if test="@oxesRef=$versenumb and notationCategories/category != 'NoNote' and notationCategories/category != 'Misc'"> <!---->
                                <xsl:text>*</xsl:text><xsl:value-of select="notationQuote/para/span"/><!--for testing <xsl:value-of select="$versenumb"/>-->
                            </xsl:if>
                        </xsl:for-each>
			<xsl:text>*</xsl:text>
                        <xsl:value-of select="./following-sibling::trGroup[1]/tr"/>
                    </xsl:if>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:for-each>
</xsl:template>
</xsl:stylesheet>

<!--
========================================================================================
Revision History
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
13-Mar-2015    Stevan Vanderwerf created initial draft for Ottoman Transcription project
========================================================================================
-->
