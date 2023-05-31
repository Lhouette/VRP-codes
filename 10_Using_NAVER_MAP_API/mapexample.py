import folium
import webbrowser

m = folium.Map(location=[37.527072, 126.973507], zoom_start=13, width=750, height=500)

m.save('map.html')
webbrowser.open_new_tab('map.html')
print('program end')