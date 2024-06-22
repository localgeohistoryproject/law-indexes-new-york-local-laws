<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/">
<xsl:for-each select="descendant::BatchRecord">
<xsl:value-of select="descendant::docClassId" />|<xsl:value-of select="descendant::propertyString[@queryName='muni_name']/value" />|<xsl:value-of select="descendant::propertyString[@queryName='muni_type']/value" />|<xsl:value-of select="descendant::propertyString[@queryName='doc_year']/value" />|<xsl:value-of select="descendant::propertyString[@queryName='law_number']/value" />|<xsl:value-of select="descendant::propertyString[@queryName='date_filed']/value" />|<xsl:value-of select="descendant::propertyString[@queryName='doc_subject']/value" />|<xsl:value-of select="DocumentAttachments/filePath" />
<xsl:text>&#xa;</xsl:text>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
