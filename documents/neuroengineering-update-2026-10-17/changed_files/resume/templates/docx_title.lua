-- Use Word's Title paragraph style for the resume name.
function Header(header)
  if header.level == 1 then
    return pandoc.Div(
      {pandoc.Para(header.content)},
      pandoc.Attr("", {}, {["custom-style"] = "Title"})
    )
  end
end

-- Keep a role heading with its first bullet across a page break.
function Para(paragraph)
  local first = paragraph.content[1]
  if first and first.t == "Strong" then
    local label = pandoc.utils.stringify(first)
    if label:find(" — ", 1, true) then
      return pandoc.Div(
        {paragraph},
        pandoc.Attr("", {}, {["custom-style"] = "Entry Heading"})
      )
    end
  end
end
