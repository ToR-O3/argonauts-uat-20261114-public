() => {
  // Read-only: no DOM writes, coordinate normalization or inconvenient rect filtering.
  const box = r => ({x:r.x,y:r.y,left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height});
  const boxes = rs => Array.from(rs, box);
  const selector = el => {
    const parts = [];
    for (let a = el; a; a = a.parentElement) {
      const siblings = a.parentElement ? Array.from(a.parentElement.children).filter(n => n.tagName === a.tagName) : [a];
      parts.unshift(a.localName + ':nth-of-type(' + (siblings.indexOf(a)+1) + ')');
    }
    return parts.join(' > ');
  };
  const styles = el => {
    const s = getComputedStyle(el);
    return Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','whiteSpace','tabSize','overflowWrap','wordBreak','overflowX','overflowY','borderLeftWidth','borderRightWidth','borderTopWidth','borderBottomWidth','paddingLeft','paddingRight','paddingTop','paddingBottom','boxSizing','color','backgroundColor','zoom'].map(k => [k,s[k]]));
  };
  const ancestor = el => {
    const r = el.getBoundingClientRect(), s = styles(el);
    // clientLeft/clientTop/clientWidth/clientHeight are native metrics, recorded
    // alongside original float border geometry. Derived padding clip kept separate.
    return {id:selector(el),rect:box(r),rects:boxes(el.getClientRects()),style:s,
      overflowX:s.overflowX,overflowY:s.overflowY,
      clientLeft:el.clientLeft,clientTop:el.clientTop,clientWidth:el.clientWidth,clientHeight:el.clientHeight,
      scrollLeft:el.scrollLeft,scrollTop:el.scrollTop,scrollWidth:el.scrollWidth,scrollHeight:el.scrollHeight,
      clip:{left:r.left+el.clientLeft,top:r.top+el.clientTop,
        right:r.left+el.clientLeft+el.clientWidth,bottom:r.top+el.clientTop+el.clientHeight}};
  };
  const targets = Array.from(document.querySelectorAll('main,h1,.metadata,.metadata-item,.label,.filename-value,.total-value,table,caption,thead,tbody,tr,th,td,.empty-message'));
  const elements = targets.map(el => {
    const all = [], full = document.createRange();
    for (let a=el.parentElement; a; a=a.parentElement) all.push(ancestor(a));
    full.selectNodeContents(el);
    return {id:selector(el),tag:el.localName,className:el.className,text:el.textContent,
      rect:box(el.getBoundingClientRect()),rects:boxes(el.getClientRects()),clip:ancestor(el).clip,
      fullRects:boxes(full.getClientRects()),style:styles(el),ancestors:all};
  });
  const texts = [];
  for (const el of targets) {
    for (let nodeIndex=0; nodeIndex<el.childNodes.length; nodeIndex++) {
      const node = el.childNodes[nodeIndex];
      if (node.nodeType !== Node.TEXT_NODE) continue;
      // Include empty and whitespace nodes for leaf targets; structural indentation
      // remains in element fullRects, not repeated as visible metadata/table text.
      if (el.children.length) continue;
      const full = document.createRange(); full.selectNodeContents(node);
      const characters = [];
      let utf16Start = 0, index = 0;
      for (const char of node.data) {
        const utf16End = utf16Start + char.length;
        const range = document.createRange();
        range.setStart(node, utf16Start); range.setEnd(node, utf16End);
        characters.push({index,utf16Start,utf16End,char,codepoint:char.codePointAt(0),rects:boxes(range.getClientRects())});
        utf16Start=utf16End; index++;
      }
      texts.push({id:selector(el)+'::text('+nodeIndex+')',owner:selector(el),nodeIndex,
        text:node.data,fullRects:boxes(full.getClientRects()),characters});
    }
  }
  return {coordinateSpace:'viewport CSS px; raw rectangles before screenshot scrolling',
    scroll:{x:scrollX,y:scrollY},viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale},
    document:{scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,
      clientWidth:document.documentElement.clientWidth,clientHeight:document.documentElement.clientHeight},
    elements,texts,dom:{basename:document.querySelector('.filename-value')?.textContent,
      total:document.querySelector('.total-value')?.textContent,
      headers:Array.from(document.querySelectorAll('th'),n=>n.textContent),
      rows:Array.from(document.querySelectorAll('tbody tr'),n=>Array.from(n.querySelectorAll('td'),t=>t.textContent)),
      empty:Array.from(document.querySelectorAll('.empty-message'),n=>n.textContent)}};
}
