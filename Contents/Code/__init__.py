c = SharedCodeService.common

###################################################################################################
def Start():
  HTTP.Headers['User-Agent'] = c.USER_AGENT
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = c.TITLE
  ObjectContainer.art = R(c.ART)
  ObjectContainer.view_group = 'List'

  DirectoryObject.art = R(c.ART)
  DirectoryObject.thumb = R(c.ICON)

  HTTP.CacheTime = CACHE_1HOUR
  

###################################################################################################
@handler('/video/theblaze', c.TITLE)
def MainMenu():

  oc = ObjectContainer()
  oc.no_cache = True

  navpage = HTML.ElementFromURL(c.SHOWS_URL,cacheTime=CACHE_1DAY)
  for show in navpage.xpath('//li[@class="show"]'):
    title      = show.xpath('.//dt')[0].text.strip()
    content_id = show.xpath('./a/@href')[0].split('content=')[1]
    thumb      = c.BASE_URL + show.xpath('.//img/@src')[0]
    summary    = show.xpath('.//p')[0].text.strip()
    oc.add(DirectoryObject(key=Callback(Playlist, content_id=content_id, title=title), title=title,summary=summary,thumb=thumb))

  oc.add(SearchDirectoryObject(identifier='com.plexapp.plugins.theblaze', title='Search', summary='Search TheBlaze Videos', prompt='Search:', thumb=R(c.ICON_SEARCH)))
  
  return oc

  
###################################################################################################
@route('/video/theblaze/playlist/{content_id}')
def Playlist(content_id, title):
    items = c.parse_search(search_text=content_id)
    oc = ObjectContainer(title2 = title)
    return c.get_clips(oc,items)

