from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """Climate change is one of the most important environmental challenges facing the world today. It refers to long-term changes in the Earth's temperature, weather patterns, and climate systems. Although the Earth's climate has naturally changed throughout history, the rapid warming observed in recent decades is mainly connected to human activities. The burning of fossil fuels, deforestation, industrial production, transportation, and other activities have increased the amount of greenhouse gases in the atmosphere.

Greenhouse gases such as carbon dioxide, methane, and nitrous oxide help keep the Earth warm by trapping some of the heat that would otherwise escape into space. This natural process is necessary for life. However, human activities have increased the concentration of these gases, causing more heat to remain in the atmosphere and increasing global temperatures.

One of the main causes of climate change is the burning of coal, oil, and natural gas. These fuels are used to produce electricity, operate factories, heat buildings, and power vehicles. When fossil fuels are burned, large amounts of carbon dioxide are released. Transportation is also a major source of emissions because cars, trucks, airplanes, and ships often depend on fossil fuels.

Deforestation is another important contributor to climate change. Trees absorb carbon dioxide from the atmosphere and store carbon as they grow. When forests are cut down or burned, this ability to absorb carbon is reduced, while some stored carbon is released into the atmosphere. Deforestation also destroys natural habitats and threatens biodiversity.

Climate change can affect almost every part of the planet. Rising temperatures can lead to more frequent or intense heat waves. Changes in rainfall patterns may cause droughts in some regions and heavy rainfall or flooding in others. These changes can create serious problems for agriculture because crops depend on suitable temperatures, water availability, and predictable seasons.

The oceans are also affected by climate change. They absorb a large amount of the additional heat caused by global warming. Warmer ocean temperatures can damage marine ecosystems, especially coral reefs. Higher temperatures can cause coral bleaching, which occurs when corals become stressed and lose the organisms that provide them with energy and color. If the stress continues, coral reefs can suffer serious damage.

Another major effect is rising sea levels. Warmer seawater expands, while melting glaciers and ice sheets add more water to the oceans. Rising sea levels can threaten coastal communities, infrastructure, agriculture, and freshwater supplies.

Climate change can also affect human health. Extreme heat can cause heat-related illnesses, while floods, storms, droughts, and wildfires can damage homes and infrastructure. Such events may also force people to leave their communities and create economic difficulties.

Addressing climate change requires cooperation between governments, businesses, communities, and individuals. Countries can invest in renewable energy such as solar and wind power, improve energy efficiency, protect forests, and develop cleaner transportation systems. Individuals can also help by reducing unnecessary energy use, limiting waste, using public transportation, and supporting environmentally responsible practices.

Climate change is a complex problem, but meaningful action is possible. Through scientific research, technological innovation, responsible policies, and cooperation, societies can reduce greenhouse gas emissions and protect the environment. The decisions made today will influence the quality of life for future generations, making climate action an important responsibility for everyone.
"""


splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=0
)


chunk = splitter.split_text(text)

print(chunk)