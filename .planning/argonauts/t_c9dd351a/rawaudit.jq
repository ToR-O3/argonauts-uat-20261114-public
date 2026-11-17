# Independent rawRange audit (no correction): per raw.json
def pos: (.width > 0 and .height > 0);
def ws: test("^[\\s\u00a0]$");
. as $r
| ($r.document.clientWidth) as $cw
| ([$r.elements[] | {key: .id, value: .clip}] | from_entries) as $clips
| [ $r.texts[] as $t
    | ($t.characters // []) as $cs
    | {
        id: $t.id,
        text_mismatch: (($cs | map(.char) | join("")) != $t.text),
        index_bad: ([range(0; $cs|length) as $i | select($cs[$i].index != $i)] | length),
        cp_bad: ([$cs[] | select((.char|explode|length) != 1 or (.char|explode[0]) != .codepoint)] | length),
        utf16_bad: ([range(0; $cs|length) as $i
                      | $cs[$i] as $c
                      | select(($c.utf16End - $c.utf16Start) != (if $c.codepoint > 65535 then 2 else 1 end)
                               or ($i > 0 and $c.utf16Start != $cs[$i-1].utf16End)
                               or ($i == 0 and $c.utf16Start != 0))] | length),
        nonblank_no_area: ([$cs[] | select((.char|ws|not) and ([.rects[]? | select(pos)] | length) == 0)] | length),
        over_right: ([$cs[] | .rects[]? | select(pos and .right > $cw)] | length),
        neg_left: ([$cs[] | .rects[]? | select(pos and .left < 0)] | length),
        clip_out: ( ($clips[$t.owner]) as $cl
                    | if $cl == null then 0 else
                      ([$cs[] | select(.char|ws|not) | .rects[]? | select(pos and (.left < $cl.left - 0.01 or .right > $cl.right + 0.01))] | length) end),
        rects: [$cs[] | select(.char|ws|not) | .rects[]? | select(pos) | [.left,.top,.right,.bottom]]
      } ]
| . as $T
| {
    texts: ($T|length),
    chars: ([$r.texts[].characters[]?] | length),
    clientWidth: $cw,
    maxRight: ([$r.texts[].characters[]?.rects[]? | select(pos) | .right] | max),
    text_mismatch: ([$T[] | select(.text_mismatch)] | length),
    index_bad: ([$T[].index_bad] | add),
    cp_bad: ([$T[].cp_bad] | add),
    utf16_bad: ([$T[].utf16_bad] | add),
    nonblank_no_area: ([$T[].nonblank_no_area] | add),
    over_right: ([$T[].over_right] | add),
    neg_left: ([$T[].neg_left] | add),
    clip_out: ([$T[].clip_out] | add),
    overlaps: ([ range(0; $T|length) as $i | range($i+1; $T|length) as $j
                 | $T[$i].rects[] as $a | $T[$j].rects[] as $b
                 | select(($a[0] < $b[2]) and ($b[0] < $a[2]) and ($a[1] < $b[3]) and ($b[1] < $a[3])
                          and ((([$a[2],$b[2]]|min) - ([$a[0],$b[0]]|max)) > 0.01)
                          and ((([$a[3],$b[3]]|min) - ([$a[1],$b[1]]|max)) > 0.01))
               ] | length)
  }
