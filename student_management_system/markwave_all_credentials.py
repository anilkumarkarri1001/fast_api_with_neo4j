markwave github credentials  :

email : anilkumark@markwave.ai
password : Anilkumar@123
Anilkumar@12345 

animalkart dashboard link : 
https://stgdash.markwave.ai/admin-list
------------------------------------------------------------->
 all animalkart dashboard credentials  :

https://stgdash.markwave.ai/orders
Superadmin 6305625580
admin 9133957450 
Employee or investor 6281507658 all otps 123456

used to login into the animalkart crm app or dashboard : 
irshad shaik => marketing manager 
9999999998


------------------------------------------------------------->
Algo,head,markwave,tail to markwave laptop

markwave salary account credentials  :

Name : Karri Anil Kumar
Employee ID : MW1045
Account Number : 015899500015371
IFSC Code : YESB0000158


 https://stgdash.markwave.ai/orders
Superadmin 6305625580

admin 9133957450 

Employee 6281507658 all otps 123456


 SWAGGER_USERNAME=markwave_admin
SWAGGER_PASSWORD=mw@swagger#2026


--------------------------------------------------------------->
database credentials :


http://neo4jstage.markwave.ai/browser/
poreddyboss
 ui-pass: ZVts79DvSvzVuw

poreddyboss
 ui-pass: Neo4jxV70DkmPcMv
--------------------------------------------------------------->

new laptop basic installtions for setup :

python 
postman 
vscode  => python installation , gitlense 
chrome 
postgre sql 
neo4j 
wps office 
antigravity and antigravity IDE

stagging database credentials  : 
http://neo4jstage.markwave.ai/browser/
ZVts79DvSvzVuw

all repositories link : 
https://github.com/orgs/markwaveai/teams/animal-kart-team/repositories 


================================================================================================>
doubts :
understand the label relation ships important : 

here what about the existing buffalos in the farm : 

 # If deactivating, block if buffaloes are currently active here
            if not payload.isActive:
                active_row = session.run(
                    """
                    MATCH (b:Buffalo)-[:ASSIGNED_TO_MARKET]->(m:Market {id: $id})
                    WHERE b.status IN ['PROCUREMENT_IN_PROGRESS', 'MARKET_QUARANTINE']
                    RETURN count(b) AS cnt
                    """,
                    id=market_id,
                ).single()
                active_count = active_row["cnt"] if active_row else 0
                if active_count > 0:
                    return {
                        "statuscode": 409,
                        "status": "error",
                        "message": (
                            f"Cannot deactivate: {active_count} buffalo(es) are currently active in this market. "
                            "Move them to the next stage first."
                        ),
                    }

                
IN NETWORKS PAGE  : 
"users": [
      {
        "id": "AK0000384",
        "mobile": "9133957450",
        "country_code": "91",
        "name": "Bhargav pamulpati",
        "total_coins": 365750.0,
        "total_redeemed_coins": 0.0,
        "total_remaining_coins": 154000.0,
        "locked_coins": 211750.0,
        "direct_locked_coins": 211750.0,
        "indirect_locked_coins": 0.0,
        "direct_referrals_coins": 365750.0,
        "indirect_referrals_coins": 0.0,
        "referral_count": 11,
        "units_purchased": 2.0,
        "role": "Admin,Investor",
        "created_date": "2026-09-05T10:42:51.039000000+05:30"
      },



        "total_coins": 365750.0,
        "total_redeemed_coins": 0.0,
        "total_remaining_coins": 154000.0,
        "locked_coins": 211750.0,
        "direct_locked_coins": 211750.0,
        "indirect_locked_coins": 0.0,
        "direct_referrals_coins": 365750.0,
        "indirect_referrals_coins": 0.0,

        why directly and indrireclty the coins are locked 


we are login with the otp verification then what is use ofthe generation ofhte jwt encoding and decoding 
i mean gen + verification where we are using the fucntioality in our appllication 



what is pip 
firebase vs superbase
what is the difference between te postgre sql and neo4j database 
why hte neo4j database best than the opstgre sql database and it is why so faster than the postgre sql database it stores the data how using the hashing will it stores the data 

what is the stcka dn heap memory , why they are intoruded and what problems acutally they are solving 
how hte variables are stored in the run time meonry using the  stcka dn heap memory
please explain the cicd pipelines flow to understand it very eaisly 
like how the code pushed and how it is deployed automatically to understnad it very eaisly 
how the s3 bucket will works to understand it very easily
how to use the redis chache in simple locally 


market_id = str(uuid.uuid4()) => why uuid is useful than the  sequential id generator 


















fixed code  :




@router.post("/incentive-approvals",
             summary="Approve the incentive for a PAID order (Marketing Manager)")
async def approve_incentive(body: IncentiveApprovalRequest,
                            x_caller_mobile: Optional[str] = Header(None),
                            verified_mobile: Optional[str] = Depends(get_verified_mobile)) -> Dict[str, Any]:
    """The single point where a MARKETING incentive is credited.

    Every check runs before db_claim_incentive_approval, so a rejected approval
    never leaves the order flagged without a matching ledger row.

    This is the marketing exec's payout ONLY. Even when this order's lead had
    a farm visit, that farm executive's payout is a separate action —
    approve_farm_incentive below — approved independently by whoever reviews
    it, on its own timeline. The two used to be bundled here (one click
    credited both), which meant a farm payout could never be reviewed or
    approved on its own.
    """
    caller_mobile = resolve_caller_mobile(x_caller_mobile, verified_mobile)
    driver = get_shared_driver()
    with driver.session() as session:
        caller = db_caller(session, caller_mobile)
        if not caller:
            raise HTTPException(status_code=404, detail="Caller not found")
        _require_incentive_approver(caller)

        order = db_order_for_approval(session, body.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Already approved: a no-op that reports the first approval.
        if order["incentive_approved"]:
            return success(
                    already_approved=True, order_id=order["order_id"],
                    approved_by=order["incentive_approved_by"],
                    approved_at=order["incentive_approved_at"])

        err = approval_error(order["paymentStatus"], order["numUnits"])
        if err:
            raise HTTPException(status_code=err[0], detail=err[1])

        # Who gets paid: the exec ASSIGNED to this order (UNIT_PLACED_BY),
        # not the investor's onboarder.  The onboarding record is still read
        # for source_type (DIRECT/INDIRECT payout rate) and lead_id, but it
        # no longer decides who receives the money.
        exec_mobile = db_order_placed_by_exec(session, order["order_id"])
        if not exec_mobile:
            raise HTTPException(
                status_code=409,
                detail="This order has no assigned marketing executive "
                       "(UNIT_PLACED_BY), so there is no one to credit")

        # Onboarding record — used only for source_type and lead_id.
        onboarding = db_order_credit_target(session, order["investor_mobile"],
                                            order_id=order["order_id"])
        source_type = onboarding["source_type"] if onboarding else ""
        if source_type not in ("DIRECT", "INDIRECT"):
            raise HTTPException(
                status_code=409,
                detail="The onboarding record has no usable source_type, so the "
                       "payout rate cannot be determined")

        # Runs with every other check, i.e. before db_claim_incentive_approval,
        # so a refused self-approval never leaves the order flagged.
        _guard_self_approval(caller, exec_mobile)

        units = whole_units(order["numUnits"])
        lead_id = order["lead_id"] or (onboarding["lead_id"] if onboarding else "")

        # Build a target-shaped dict so the rest of the function is unchanged.
        target = {"exec_mobile": exec_mobile, "source_type": source_type,
                  "lead_id": lead_id}

        # The plan that will price this credit, checked BEFORE the claim below.
        # process_close_incentives used to discover a missing plan on the far
        # side of the point of no return and skip the ledger row silently,
        # leaving the order flagged approved with nothing credited and its
        # units invisible to every later order's slab position. Approval is
        # one-way, so that loss can never be corrected — it has to be refused
        # here instead. See utils/marketing_incentive.plan_error.
        now = _now_iso()
        # The month this credit belongs to — the ORDER's approval, not this
        # moment. A batch sign-off must not drag an August sale into
        # September's slab ladder (incentive_period_basis).
        period_on = incentive_period_basis(order.get("order_approved_at", ""), now)
        try:
            period_day = incentive_period_date(period_on)
        except (TypeError, ValueError):
            period_day = _today_ist()
        perr = plan_error(
            db_plan_for_month(session, "MONTHLY",
                              period_day.year, period_day.month),
            period_day.strftime("%Y-%m"))
        if perr:
            raise HTTPException(status_code=perr[0], detail=perr[1])

        # Point of no return.
        if not db_claim_incentive_approval(session, order["order_id"],
                                           caller["mobile"], now):
            # Another request won the race, or the order left PAID underneath us.
            fresh = db_order_for_approval(session, order["order_id"]) or {}
            return success(
                    already_approved=True, order_id=order["order_id"],
                    approved_by=fresh.get("incentive_approved_by", ""),
                    approved_at=fresh.get("incentive_approved_at", ""))

        exec_mobile = target["exec_mobile"]
        db_increment_targets(session, exec_mobile, units=units)
        credit = process_close_incentives(session, exec_mobile, units,
                                          target["source_type"], lead_id,
                                          order_id=order["order_id"],
                                          approved_at=now, period_on=period_on)

        # Only the FIRST paid order for a lead closes it; a legacy lead that is
        # already Closed still credits its units.
        lead_closed = False
        if lead_id and db_lead_status(session, lead_id) not in (None, "Closed"):
            db_close_lead(session, lead_id, units, caller, now)
            lead_closed = True

    return success(already_approved=False,
            order_id=order["order_id"], units=units,
            credited_to=exec_mobile, source_type=target["source_type"],
            lead_id=lead_id, lead_closed=lead_closed,
            approved_by=caller["mobile"], approved_at=now,
            incentive=credit)