/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.entity;

/**
 *
 * @author winsxx
 */
public class TradeOffer {
    public long offeredItem;
    public long offeredAmmount;
    public long demandedItem;
    public long demandedAmmount;
    public boolean availability;
    private final String offerToken;
    
    public TradeOffer(String offerToken){
        this.offerToken = offerToken;
        this.offeredItem = 0;
        this.offeredAmmount = 0;
        this.demandedItem = 0;
        this.demandedAmmount = 0;
        this.availability = false;
    }
    
    public TradeOffer(String offerToken, long offeredItem, long offeredAmmount, long demandedItem, long demandedAmmount, boolean avaliablity){
        
        this.offerToken = offerToken;
        this.offeredItem = offeredItem;
        this.offeredAmmount = offeredAmmount;
        this.demandedItem = demandedItem;
        this.demandedAmmount = demandedAmmount;
        this.availability = availability;
    }
}
