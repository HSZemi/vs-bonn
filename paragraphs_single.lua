-- This is a sample custom writer for pandoc.  It produces output
-- that is very similar to that of pandoc's HTML writer.
-- There is one new feature: code blocks marked with class 'dot'
-- are piped through graphviz and images are included in the HTML
-- output using 'data:' URLs.
--
-- Invoke with: pandoc -t sample.lua
--
-- Note:  you need not have lua installed on your system to use this
-- custom writer.  However, if you do have lua installed, you can
-- use it to test changes to the script.  'lua sample.lua' will
-- produce informative error messages if your code contains
-- syntax errors.

-- Character escaping
local function escape(s, in_attribute)
  return s:gsub("[<>&\"']",
    function(x)
      if x == '<' then
        return '&lt;'
      elseif x == '>' then
        return '&gt;'
      elseif x == '&' then
        return '&amp;'
      elseif x == '"' then
        return '&quot;'
      elseif x == "'" then
        return '&#39;'
      else
        return x
      end
    end)
end

-- Helper function to convert an attributes table into
-- a string that can be put into HTML tags.
local function attributes(attr)
  local attr_table = {}
  for x,y in pairs(attr) do
    if y and y ~= "" then
      table.insert(attr_table, ' ' .. x .. '="' .. escape(y,true) .. '"')
    end
  end
  return table.concat(attr_table)
end


-- Helper function that extracts the paragraph number from a heading.
-- If there is none, the regular id is returned.
local function paragraph_id(s, attr)
  local id = string.match(s, '^§ ([0-9]+)')
  if id == nil then
    return attr.id
  end
  return '§' .. id
end

-- Run cmd on a temporary file containing inp and return result.
local function pipe(cmd, inp)
  local tmp = os.tmpname()
  local tmph = io.open(tmp, "w")
  tmph:write(inp)
  tmph:close()
  local outh = io.popen(cmd .. " " .. tmp,"r")
  local result = outh:read("*all")
  outh:close()
  os.remove(tmp)
  return result
end

-- Table to store footnotes, so they can be included at the end.
local notes = {}

-- Table to store toc.
local toc = {}
local lastlev = 1

-- Blocksep is used to separate block elements.
function Blocksep()
  return "\n\n"
end

-- This function is called once for the whole document. Parameters:
-- body is a string, metadata is a table, variables is a table.
-- One could use some kind of templating
-- system here; this just gives you a simple standalone HTML file.
function Doc(body, metadata, variables)
  local buffer = {}
  local function add(s)
    table.insert(buffer, s)
  end
--  add('<div class="container">')
  add('{navigation}')
  if metadata['title'] and metadata['short'] and metadata['title'] ~= "" then
    add('<h1 class="title" title="' .. metadata['title'] .. '">' .. metadata['short'] .. '</h1>')
  end
  for _, author in pairs(metadata['author'] or {}) do
    add('<h2 class="author">' .. author .. '</h2>')
  end
  if metadata['date'] and metadata['date'] ~= "" then
    add('<h3 class="date">Fassung vom ' .. metadata.date .. ' (<a href="#contains">?</a>)</h3>')
  end
   if #toc > 0 then
    add('<h3>Inhaltsverzeichnis <span id="toctoggle" class="eye-open" aria-hidden="true" onclick="toggleTOC()"></span></h3>')
    add('<script type="text/javascript" src="{path_to_top}toc.js"></script>')
    add('<ol id="toc" class="toc">')
    for _,item in pairs(toc) do
      add(item)
    end
    while lastlev > 1 do
      add('</ol>')
      lastlev = lastlev - 1
    end
    add('</ol>')
  end
  add(body)
  if #notes > 0 then
    add('<hr>')
    add('<ol class="footnotes">')
    for _,note in pairs(notes) do
      add(note)
    end
    add('</ol>')
  end
  if metadata['contains'] then
    add('<hr>')
    add(containsBox(metadata['contains']))
  end
  --  add('</div>')
  return table.concat(buffer,'\n')
end

-- The functions that follow render corresponding pandoc elements.
-- s is always a string, attr is always a table of attributes, and
-- items is always an array of strings (the items in a list).
-- Comments indicate the types of other variables.

function containsBox(contains)
  local buffer = {}
  table.insert(buffer, "<div id='contains'>")
  table.insert(buffer, "<p>Diese Gesamtfassung enth&auml;lt folgende Dokumente:</p>")
  for _,source in pairs(contains) do
    table.insert(buffer, "<table class='table table-bordered'>")
    table.insert(buffer, "<tr><td><b>Titel</b></td>")
    table.insert(buffer, "<td title='"..source.title.."'><b>"..source.short.."</b></td></tr>")
    table.insert(buffer, "<tr><td>Beschlussorgan</td>")
    table.insert(buffer, "<td>"..source.actorgan.."</td></tr>")
    table.insert(buffer, "<tr><td>Beschlussdatum</td>")
    table.insert(buffer, "<td>"..source.actdate.."</td></tr>")
    if source.confirmorgan and source.confirmdate then
      table.insert(buffer, "<tr><td>Best&auml;tigungsorgan</td>")
      table.insert(buffer, "<td>"..source.confirmorgan.."</td></tr>")
      table.insert(buffer, "<tr><td>Best&auml;tigungsdatum</td>")
      table.insert(buffer, "<td>"..source.confirmdate.."</td></tr>")
    end
    table.insert(buffer, "<tr><td>Publikationsorgan</td>")
    table.insert(buffer, "<td>"..source.puborgan.."</td></tr>")
    table.insert(buffer, "<tr><td>Publikationsdatum</td>")
    table.insert(buffer, "<td>"..source.pubdate.."</td></tr>")
    table.insert(buffer, "<tr><td>URL</td>")
    table.insert(buffer, "<td><a href='"..source.puburl.."'>"..source.puburl.."</a></td></tr>")
    table.insert(buffer, "</table>")
  end
  table.insert(buffer, "</div>")
  return table.concat(buffer, "\n")
end

function RawInline(type,s)
  return Str(s)
end

function Str(s)
  return escape(s)
end

function Space()
  return " "
end

function LineBreak()
  return "<br/>"
end

function Emph(s)
  return "<em>" .. s .. "</em>"
end

function Strong(s)
  return "<strong>" .. s .. "</strong>"
end

function Subscript(s)
  return "<sub>" .. s .. "</sub>"
end

function Superscript(s)
  return "<sup>" .. s .. "</sup>"
end

function SmallCaps(s)
  return '<span style="font-variant: small-caps;">' .. s .. '</span>'
end

function Strikeout(s)
  return '<del>' .. s .. '</del>'
end

function Link(s, src, tit)
  return "<a href='" .. escape(src,true) .. "' title='" ..
         escape(tit,true) .. "'>" .. s .. "</a>"
end

function Image(s, src, tit)
  return "<img src='" .. escape(src,true) .. "' title='" ..
         escape(tit,true) .. "'/>"
end

function Code(s, attr)
  return "<code" .. attributes(attr) .. ">" .. escape(s) .. "</code>"
end

function InlineMath(s)
  return "\\(" .. escape(s) .. "\\)"
end

function DisplayMath(s)
  return "\\[" .. escape(s) .. "\\]"
end

function SoftBreak(s)
  return "\n"
end

function Note(s)
  local num = #notes + 1
  -- insert the back reference right before the final closing tag.
  s = string.gsub(s,
          '(.*)</', '%1 <a href="#fnref' .. num ..  '">&#8617;</a></')
  -- add a list item with the note to the note table.
  table.insert(notes, '<li id="fn' .. num .. '">' .. s .. '</li>')
  -- return the footnote reference, linked to the note.
  return '<a id="fnref' .. num .. '" href="#fn' .. num ..
            '"><sup>' .. num .. '</sup></a>'
end

function Span(s, attr)
  return "<span" .. attributes(attr) .. ">" .. s .. "</span>"
end

function Cite(s)
  return "<span class=\"cite\">" .. s .. "</span>"
end

function Plain(s)
  return s
end

function Para(s)
  return "<p>" .. s .. "</p>"
end

-- lev is an integer, the header level.
function Header(lev, s, attr)
  attr.id = paragraph_id(s, attr)
  while lastlev < lev do
    table.insert(toc, '<ol>')
    lastlev = lastlev + 1
  end
  while lastlev > lev do
    table.insert(toc, '</ol>')
    lastlev = lastlev - 1
  end
  table.insert(toc, '<li><a href="#'  ..  attr.id..'">' .. s .. '</a></li>')
  return "<h" .. lev .. attributes(attr) ..  ">" .. s .. "<a class=\"anchor\" href=\"#" .. attr.id .. "\"><img class='anchorimage' src='{path_to_top}chain.svg' /></a></h" .. lev .. ">"
end

function BlockQuote(s)
  return "<blockquote>\n" .. s .. "\n</blockquote>"
end

function HorizontalRule()
  return "<hr/>"
end

function CodeBlock(s, attr)
  -- If code block has class 'dot', pipe the contents through dot
  -- and base64, and include the base64-encoded png as a data: URL.
  if attr.class and string.match(' ' .. attr.class .. ' ',' dot ') then
    local png = pipe("base64", pipe("dot -Tpng", s))
    return '<img src="data:image/png;base64,' .. png .. '"/>'
  -- otherwise treat as code (one could pipe through a highlighter)
  else
    return "<pre><code" .. attributes(attr) .. ">" .. escape(s) ..
           "</code></pre>"
  end
end


function BulletList(items)
  local buffer = {}
  for _, item in pairs(items) do
    table.insert(buffer, "<li>" .. item .. "</li>")
  end
  return "<ul>\n" .. table.concat(buffer, "\n") .. "\n</ul>"
end

function OrderedList(items, start, type, itemstyle)
  local buffer = {}
  for _, item in pairs(items) do
    table.insert(buffer, "<li>" .. item .. "</li>")
  end
  return "<ol start=\"" .. start .. "\" class=\"" .. type .. "\">\n" .. table.concat(buffer, "\n") .. "\n</ol>"
end

-- Revisit association list STackValue instance.
function DefinitionList(items)
  local buffer = {}
  for _,item in pairs(items) do
    for k, v in pairs(item) do
      table.insert(buffer,"<dt>" .. k .. "</dt>\n<dd>" ..
                        table.concat(v,"</dd>\n<dd>") .. "</dd>")
    end
  end
  return "<dl>\n" .. table.concat(buffer, "\n") .. "\n</dl>"
end

-- Convert pandoc alignment to something HTML can use.
-- align is AlignLeft, AlignRight, AlignCenter, or AlignDefault.
function html_align(align)
  if align == 'AlignLeft' then
    return 'left'
  elseif align == 'AlignRight' then
    return 'right'
  elseif align == 'AlignCenter' then
    return 'center'
  else
    return 'left'
  end
end

-- Caption is a string, aligns is an array of strings,
-- widths is an array of floats, headers is an array of
-- strings, rows is an array of arrays of strings.
function Table(caption, aligns, widths, headers, rows)
  local buffer = {}
  local function add(s)
    table.insert(buffer, s)
  end
  add("<table>")
  if caption ~= "" then
    add("<caption>" .. caption .. "</caption>")
  end
  if widths and widths[1] ~= 0 then
    for _, w in pairs(widths) do
      add('<col width="' .. string.format("%d%%", w * 100) .. '" />')
    end
  end
  local header_row = {}
  local empty_header = true
  for i, h in pairs(headers) do
    local align = html_align(aligns[i])
    table.insert(header_row,'<th align="' .. align .. '">' .. h .. '</th>')
    empty_header = empty_header and h == ""
  end
  if empty_header then
    head = ""
  else
    add('<tr class="header">')
    for _,h in pairs(header_row) do
      add(h)
    end
    add('</tr>')
  end
  local class = "even"
  for _, row in pairs(rows) do
    class = (class == "even" and "odd") or "even"
    add('<tr class="' .. class .. '">')
    for i,c in pairs(row) do
      add('<td align="' .. html_align(aligns[i]) .. '">' .. c .. '</td>')
    end
    add('</tr>')
  end
  add('</table>')
  return table.concat(buffer,'\n')
end

function Div(s, attr)
  return "<div" .. attributes(attr) .. ">\n" .. s .. "</div>"
end

-- The following code will produce runtime warnings when you haven't defined
-- all of the functions you need for the custom writer, so it's useful
-- to include when you're working on a writer.
local meta = {}
meta.__index =
  function(_, key)
    io.stderr:write(string.format("WARNING: Undefined function '%s'\n",key))
    return function() return "" end
  end
setmetatable(_G, meta)
