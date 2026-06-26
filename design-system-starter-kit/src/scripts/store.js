// Bovine TB prototype — small client-side session store.
//
// Persists vaccinations logged during the session (sessionStorage) so updates
// are reflected on EVERY page (list, record, flow). This is the prototype
// stand-in for the Salesforce database; in a real org these are related records
// and every page simply re-queries them.
//
// sessionStorage = lasts for the browser tab/session and clears when closed.
// Swap to localStorage below if you want it to persist across restarts.
(function (w) {
  var KEY = 'bovinetb_session';
  var box = w.sessionStorage;

  function read() {
    try { return JSON.parse(box.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function write(obj) {
    try { box.setItem(KEY, JSON.stringify(obj)); } catch (e) {}
  }

  w.VaxStore = {
    // Add a vaccination record for an animal (keyed by ear tag).
    add: function (tag, rec) {
      var s = read();
      if (!s[tag]) s[tag] = [];
      s[tag].push(rec);
      write(s);
    },

    // Session-logged records for one animal, newest first.
    forTag: function (tag) {
      return (read()[tag] || []).slice().reverse();
    },

    // Merge session records into a cattle array: prepend newly logged
    // vaccinations and reflect the change in 'last' and 'status' so the list
    // and record pages stay in sync.
    apply: function (cattle) {
      var s = read();
      cattle.forEach(function (c) {
        var recs = s[c.tag] || [];
        if (recs.length) {
          var newest = recs.slice().reverse();
          c.vax = newest.concat(c.vax || []);
          c.last = newest[0].date;
          c.status = 'Vaccinated';
        }
      });
      return cattle;
    },

    // Clear all session-entered data (reset the demo).
    reset: function () { try { box.removeItem(KEY); } catch (e) {} }
  };
})(window);
